"""YOLOv11-OBB with SAHI tiled inference for marine radar detection."""

from pathlib import Path

import numpy as np
import torch
import yaml


def train_yolov11(
    data_yaml: str | Path,
    config_path: str | Path,
    output_dir: str | Path,
    seed: int = 42,
):
    """Train YOLOv11-OBB model.

    Args:
        data_yaml: Path to YOLO-format data config.
        config_path: Path to model config YAML.
        output_dir: Directory for training outputs.
        seed: Random seed.
    """
    from ultralytics import YOLO

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    model = YOLO(cfg["model"]["variant"] + ".pt")

    train_cfg = cfg["training"]
    aug_cfg = cfg.get("augmentation", {})

    model.train(
        data=str(data_yaml),
        epochs=train_cfg["epochs"],
        batch=train_cfg["batch_size"],
        imgsz=train_cfg["imgsz"],
        optimizer=train_cfg["optimizer"],
        lr0=train_cfg["lr0"],
        lrf=train_cfg["lrf"],
        warmup_epochs=train_cfg["warmup_epochs"],
        patience=train_cfg["patience"],
        device=train_cfg["device"],
        workers=train_cfg["workers"],
        seed=seed,
        project=str(output_dir),
        name=f"yolov11_seed{seed}",
        hsv_h=aug_cfg.get("hsv_h", 0.015),
        hsv_s=aug_cfg.get("hsv_s", 0.7),
        hsv_v=aug_cfg.get("hsv_v", 0.4),
        flipud=aug_cfg.get("flipud", 0.5),
        fliplr=aug_cfg.get("fliplr", 0.5),
        mosaic=aug_cfg.get("mosaic", 1.0),
        mixup=aug_cfg.get("mixup", 0.1),
    )
    return model


def predict_yolov11(
    model_path: str | Path,
    image: np.ndarray,
    conf: float = 0.25,
    device: str = "0",
) -> np.ndarray:
    """Run YOLOv11-OBB inference on a single image.

    Returns:
        (N, 5) array of [x1, y1, x2, y2, confidence].
    """
    from ultralytics import YOLO

    model = YOLO(str(model_path))
    results = model.predict(image, conf=conf, device=device, verbose=False)

    if len(results) == 0 or results[0].boxes is None:
        return np.zeros((0, 5), dtype=np.float32)

    boxes = results[0].boxes.xyxy.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy().reshape(-1, 1)
    return np.hstack([boxes, confs])


def predict_sahi(
    model_path: str | Path,
    image_path: str | Path,
    config_path: str | Path,
) -> list[dict]:
    """Run SAHI tiled inference with YOLOv11-OBB.

    Returns:
        List of prediction dicts with 'bbox' and 'score' keys.
    """
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    sahi_cfg = cfg["sahi"]

    detection_model = AutoDetectionModel.from_pretrained(
        model_type="ultralytics",
        model_path=str(model_path),
        confidence_threshold=0.25,
        device="cuda:0",
    )

    result = get_sliced_prediction(
        str(image_path),
        detection_model,
        slice_height=sahi_cfg["slice_height"],
        slice_width=sahi_cfg["slice_width"],
        overlap_height_ratio=sahi_cfg["overlap_height_ratio"],
        overlap_width_ratio=sahi_cfg["overlap_width_ratio"],
        postprocess_type=sahi_cfg["postprocess_type"],
        postprocess_match_threshold=sahi_cfg["postprocess_match_threshold"],
    )

    predictions = []
    for pred in result.object_prediction_list:
        predictions.append({
            "bbox": pred.bbox.to_xyxy(),
            "score": pred.score.value,
            "category": pred.category.name,
        })

    return predictions
