"""RT-DETR: Real-Time DEtection TRansformer for marine radar (NMS-free)."""

from pathlib import Path

import numpy as np
import yaml


def train_rt_detr(
    data_yaml: str | Path,
    config_path: str | Path,
    output_dir: str | Path,
    seed: int = 42,
):
    """Train RT-DETR model using Ultralytics.

    Args:
        data_yaml: Path to YOLO-format data config.
        config_path: Path to model config YAML.
        output_dir: Directory for training outputs.
        seed: Random seed.
    """
    from ultralytics import RTDETR

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    model = RTDETR(cfg["model"]["variant"] + ".pt")

    train_cfg = cfg["training"]
    aug_cfg = cfg.get("augmentation", {})

    model.train(
        data=str(data_yaml),
        epochs=train_cfg["epochs"],
        batch=train_cfg["batch_size"],
        imgsz=train_cfg["imgsz"],
        optimizer=train_cfg["optimizer"],
        lr0=train_cfg["lr"],
        warmup_epochs=train_cfg["warmup_epochs"],
        device=train_cfg["device"],
        workers=train_cfg["workers"],
        seed=seed,
        project=str(output_dir),
        name=f"rtdetr_seed{seed}",
        flipud=aug_cfg.get("flipud", 0.5),
        fliplr=aug_cfg.get("fliplr", 0.5),
        mosaic=aug_cfg.get("mosaic", 0.5),
    )
    return model


def predict_rt_detr(
    model_path: str | Path,
    image: np.ndarray,
    conf: float = 0.25,
    device: str = "0",
) -> np.ndarray:
    """Run RT-DETR inference.

    Returns:
        (N, 5) array of [x1, y1, x2, y2, confidence].
    """
    from ultralytics import RTDETR

    model = RTDETR(str(model_path))
    results = model.predict(image, conf=conf, device=device, verbose=False)

    if len(results) == 0 or results[0].boxes is None:
        return np.zeros((0, 5), dtype=np.float32)

    boxes = results[0].boxes.xyxy.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy().reshape(-1, 1)
    return np.hstack([boxes, confs])
