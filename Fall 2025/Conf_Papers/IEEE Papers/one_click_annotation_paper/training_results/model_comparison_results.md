# Model Comparison Results - RADAR3000 Dataset

## Summary Table (Ranked by mAP50)

| Rank | Model | Image Size | Epochs | mAP50 | mAP50-95 | Precision | Recall | Status |
|------|-------|------------|--------|-------|----------|-----------|--------|--------|
| 🥇 | MRISNET (Segmentation) | N/A | N/A | **0.9350** | 0.4520 | 0.952 | 0.948 | Published |
| 🥈 | YOLOv12-L (Single) | 1024x1024 | 150 | **0.9277** | 0.4250 | 0.9057 | 0.8862 | Complete |
| 🥉 | YOLOv12-L (DDP) | 1024x1024 | 150 | **0.9246** | 0.4202 | 0.9024 | 0.8861 | Complete |
| 4 | SO-DETR (R18) | 1024x1024 | 150 | **0.9194** | 0.3991 | 0.9039 | 0.9082 | Complete |
| 5 | RF-DETR (Base) | 1008x1008 | 50 | **0.9102** | 0.4087 | 0.9167 | 0.89 | Complete |
| 6 | YOLOv8n + SSL | 640x640 | 50 | **0.8960** | 0.4020 | 0.874 | 0.843 | Complete |
| 7 | MS-DETR (Deformable) | 800x800 | 50 | **0.8773** | 0.3448 | - | - | Complete |

## Key Findings

1. **MRISNET** achieves highest mAP50 (0.935) but is for **instance segmentation** (different task)
2. **YOLOv12-L** achieves best **object detection** results (0.925-0.928 mAP50) with 150 epochs
3. **SO-DETR** performs competitively (0.919 mAP50) with DETR-based architecture
4. **RF-DETR** achieves strong results (0.910 mAP50) with only 50 epochs
5. **MS-DETR** shows good results (0.877 mAP50) with smaller 800px images

## Training Notes

| Model | Framework | Epochs | Batch Size | Learning Rate | Notes |
|-------|-----------|--------|------------|---------------|-------|
| YOLOv12-L | Ultralytics | 150 | 18 | 0.01 | AMP enabled |
| SO-DETR | Ultralytics | 150 | 18 | 0.01 | AMP disabled (FFT) |
| RF-DETR | RF-DETR | 50 | 2 | 1e-4 | 1008px resolution |
| MS-DETR | HuggingFace | 50 | 4 | 1e-5 | Pretrained backbone |
| YOLOv8+SSL | Ultralytics | 50 | - | - | SimCLR pretrained |

## Dataset: RADAR3000

- **Total Images**: 3,000
- **Train/Val/Test**: 2,400 / 600 / 600
- **Classes**: 1 (radar object detection)

---
*Report generated: 2024-12-12*
