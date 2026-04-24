# Classical vs. Deep Learning Object Detection in X-Band Marine Radar Imagery

A cross-paradigm benchmark of 8 object detection methods — 4 classical and 4 deep learning — on the DLR DAAN / DARC / MANV corpus.

**Authors:** J.C. Vaught and Ty Dangerfield — University of South Carolina CSCE 763.
**Paper:** [`report/radar_detection_report.pdf`](report/radar_detection_report.pdf)
**Data:** [release `data-v1.0`](https://github.com/j-vaught/marine-radar-detection/releases/tag/data-v1.0)

## Methods

Each method is a self-contained folder under `src/`. Owners are free to reshape inputs however they want — the only shared inputs are the COCO-format annotations and PPI images shipped in the data release.

| Folder | Methods | Entry point(s) |
|---|---|---|
| `src/cfar/` | CA / GO / SO / OS-CFAR | `run.py` |
| `src/morphological/` | Otsu + opening/closing + CC | `run.py` |
| `src/otsu/` | Otsu, SSOTSU | `run.py` |
| `src/wavelet/` | Stationary wavelet transform (db4, 3 levels) | `run.py` |
| `src/yolo/` | YOLOv11 (Ultralytics) | `train.py`, `infer.py`, `coco_to_yolo.py` |
| `src/rtdetr/` | RT-DETR (Ultralytics) | `train.py`, `infer.py`, `coco_to_yolo.py` |
| `src/faster_rcnn/` | Faster R-CNN (torchvision) | `train.py`, `infer.py`, `dataset.py` |
| `src/unet/` | U-Net segmentation | `train.py`, `infer.py`, `dataset.py` |

Each folder also contains a `config.yaml` (hyperparameters) and a `detector.py` or `model.py` (core logic).

## Project structure

```
marine-radar-detection/
├── data/
│   ├── raw/HAXR/              # 5.1 GB — kept for future work
│   └── processed/
│       ├── images/            # 2,239 PPI PNGs (from data-v1.0)
│       └── annotations/       # COCO JSONs (full + tiled)
├── dist/                      # gitignored — release tarballs
├── report/                    # Typst source + compiled PDFs
├── src/
│   ├── cfar/ morphological/ otsu/ wavelet/          # classical
│   └── yolo/ rtdetr/ faster_rcnn/ unet/             # deep learning
├── pyproject.toml
└── README.md
```

No shared `common/`, `eval/`, `scripts/`, `configs/`, or `Makefile`. Each method folder is self-contained so a teammate can take ownership of one detector without touching anyone else's code. Helper functions (circular PPI mask, COCO → YOLO conversion, pycocotools AP) are inlined per folder; ~200 lines of intentional duplication buys team sovereignty.

## Setup

Requires Python 3.10+ and (for DL) CUDA 12.4.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install -e ".[dev]"
```

## Fetch the dataset

```bash
curl -LO https://github.com/j-vaught/marine-radar-detection/releases/download/code-v1.1/processed-v1.tar.zst
curl -LO https://github.com/j-vaught/marine-radar-detection/releases/download/code-v1.1/processed-v1.tar.zst.sha256
sha256sum -c processed-v1.tar.zst.sha256
zstd -dc processed-v1.tar.zst | tar -xf - -C data/
```

This populates `data/processed/images/` (2,239 PPI PNGs) and `data/processed/annotations/all.json` — the full AIS-anchored ground truth in one COCO file, unsplit. You decide train/val/test however you want (the paper uses filename prefix: MANV → train, DARC → val, DAAN → test). Tiling, YOLO-format conversion, mask generation, and any format munging are also your call.

## Running a method

Every method folder runs as a Python module. You hand it whichever COCO JSON + image directory you built.

**Classical detectors** — single command, prints COCO AP at the end. The example below evaluates on the full corpus; substitute your own test split if you split the data:

```bash
python -m src.cfar.run          --ann data/processed/annotations/all.json --images data/processed/images --variant ca_cfar
python -m src.morphological.run --ann data/processed/annotations/all.json --images data/processed/images
python -m src.otsu.run          --ann data/processed/annotations/all.json --images data/processed/images --variant ssotsu
python -m src.wavelet.run       --ann data/processed/annotations/all.json --images data/processed/images
```

**Deep learning detectors** — train then infer. Each folder takes explicit train/val paths so you can use whatever split + tiling layout you produced:

```bash
# YOLO / RT-DETR need YOLO-format labels; supply your own split files
python -m src.yolo.coco_to_yolo \
    --train-ann <your_train.json> --val-ann <your_val.json> --test-ann <your_test.json> \
    --train-images <your_train_dir> --val-images <your_val_dir> --test-images <your_test_dir> \
    --out data/processed/yolo

python -m src.yolo.train  --data data/processed/yolo/data.yaml
python -m src.yolo.infer  --weights results/yolo/best_seed42.pt \
                          --ann <your_test.json> --images <your_test_dir>

# Faster R-CNN
python -m src.faster_rcnn.train \
    --train-ann <your_train.json> --val-ann <your_val.json> \
    --train-images <your_train_dir> --val-images <your_val_dir>

# U-Net (segmentation — needs paired image + binary-mask directories you build yourself)
python -m src.unet.train \
    --train-images <your_train_images> --train-masks <your_train_masks> \
    --val-images   <your_val_images>   --val-masks   <your_val_masks>
```

Each `infer.py` / `run.py` writes a `results/<method>/*_predictions.json` and prints a COCO AP summary via pycocotools. No central evaluation step.

## Reproducing the paper

The PDF at [`report/radar_detection_report.pdf`](report/radar_detection_report.pdf) corresponds to the AIS-anchored GT, calibration, and paper's split convention (MANV/DARC/DAAN → train/val/test). All detector hyperparameters live in each method's `config.yaml`.

Typst source:

```bash
typst compile report/report.typ report/radar_detection_report.pdf
```
