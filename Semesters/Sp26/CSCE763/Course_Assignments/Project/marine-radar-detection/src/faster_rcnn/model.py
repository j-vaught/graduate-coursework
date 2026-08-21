"""Marine-Faster R-CNN with radar-specific anchor optimization."""

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import yaml
from torch.utils.data import DataLoader
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from tqdm import tqdm


def build_model(cfg: dict) -> nn.Module:
    """Build Faster R-CNN with radar-optimized anchors.

    Args:
        cfg: Model config dict.

    Returns:
        Faster R-CNN model.
    """
    from torchvision.models.detection.rpn import AnchorGenerator

    model_cfg = cfg["model"]

    anchor_sizes = tuple(tuple(s) for s in model_cfg["anchor_sizes"])
    anchor_ratios = tuple(tuple(r) for r in model_cfg["anchor_ratios"]) * len(anchor_sizes)

    anchor_generator = AnchorGenerator(sizes=anchor_sizes, aspect_ratios=anchor_ratios)

    model = fasterrcnn_resnet50_fpn(
        weights="DEFAULT",
        rpn_anchor_generator=anchor_generator,
        rpn_pre_nms_top_n_train=model_cfg["rpn_pre_nms_top_n_train"],
        rpn_post_nms_top_n_train=model_cfg["rpn_post_nms_top_n_train"],
        rpn_pre_nms_top_n_test=model_cfg["rpn_pre_nms_top_n_test"],
        rpn_post_nms_top_n_test=model_cfg["rpn_post_nms_top_n_test"],
        rpn_nms_thresh=model_cfg["rpn_nms_thresh"],
        rpn_fg_iou_thresh=model_cfg["rpn_fg_iou_thresh"],
        rpn_bg_iou_thresh=model_cfg["rpn_bg_iou_thresh"],
        box_score_thresh=model_cfg["box_score_thresh"],
        box_nms_thresh=model_cfg["box_nms_thresh"],
        box_detections_per_img=model_cfg["box_detections_per_img"],
    )

    # Replace head for correct number of classes
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, model_cfg["num_classes"])

    return model


def train_faster_rcnn(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    cfg: dict,
    output_dir: str | Path,
    seed: int = 42,
):
    """Train Faster R-CNN model.

    Args:
        model: Faster R-CNN model.
        train_loader: Training data loader.
        val_loader: Validation data loader.
        cfg: Full config dict.
        output_dir: Output directory.
        seed: Random seed.
    """
    torch.manual_seed(seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_cfg = cfg["training"]
    device = torch.device(f"cuda:{train_cfg['device']}" if torch.cuda.is_available() else "cpu")
    model.to(device)

    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(
        params,
        lr=train_cfg["lr"],
        momentum=train_cfg["momentum"],
        weight_decay=train_cfg["weight_decay"],
    )
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer,
        step_size=train_cfg["lr_step_size"],
        gamma=train_cfg["lr_gamma"],
    )

    best_loss = float("inf")

    for epoch in range(train_cfg["epochs"]):
        model.train()
        epoch_loss = 0.0

        pbar = tqdm(train_loader, desc=f"Epoch {epoch + 1}/{train_cfg['epochs']}")
        for images, targets in pbar:
            images = [img.to(device) for img in images]
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss_dict.values())

            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            epoch_loss += losses.item()
            pbar.set_postfix(loss=losses.item())

        scheduler.step()
        avg_loss = epoch_loss / len(train_loader)

        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), output_dir / f"best_seed{seed}.pth")

        torch.save(model.state_dict(), output_dir / f"last_seed{seed}.pth")

    return model


def predict_faster_rcnn(
    model: nn.Module,
    image: torch.Tensor,
    device: str = "cuda:0",
    score_thresh: float = 0.5,
) -> np.ndarray:
    """Run inference with Faster R-CNN.

    Returns:
        (N, 5) array of [x1, y1, x2, y2, score].
    """
    model.eval()
    model.to(device)

    with torch.no_grad():
        prediction = model([image.to(device)])[0]

    boxes = prediction["boxes"].cpu().numpy()
    scores = prediction["scores"].cpu().numpy()

    keep = scores >= score_thresh
    boxes = boxes[keep]
    scores = scores[keep].reshape(-1, 1)

    return np.hstack([boxes, scores]) if len(boxes) > 0 else np.zeros((0, 5), dtype=np.float32)
