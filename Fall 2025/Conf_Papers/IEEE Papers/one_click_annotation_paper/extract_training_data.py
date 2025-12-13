#!/usr/bin/env python3
"""
Extract training data from various model training outputs and prepare for TikZ plotting.
"""
import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Paths
RESULTS_DIR = Path(__file__).parent / "training_results"

def extract_yolov12(model_name: str, training_type: str = "single") -> List[Dict]:
    """Extract YOLOv12 training data from CSV."""
    csv_path = RESULTS_DIR / "yolov12" / f"train_{training_type}_150epochs" / "results.csv"

    data = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'epoch': int(row['epoch']),
                'train_loss': float(row['train/box_loss']) + float(row['train/cls_loss']) + float(row['train/dfl_loss']),
                'val_loss': float(row['val/box_loss']) + float(row['val/cls_loss']) + float(row['val/dfl_loss']),
                'mAP50': float(row['metrics/mAP50(B)']),
                'mAP50_95': float(row['metrics/mAP50-95(B)']),
                'precision': float(row['metrics/precision(B)']),
                'recall': float(row['metrics/recall(B)']),
            })
    return data

def extract_so_detr() -> List[Dict]:
    """Extract SO-DETR training data from CSV."""
    csv_path = RESULTS_DIR / "so_detr" / "train_ddp" / "results.csv"

    data = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip whitespace from keys
            clean_row = {k.strip(): v for k, v in row.items()}
            data.append({
                'epoch': int(float(clean_row['epoch'])),
                'train_loss': float(clean_row['train/giou_loss']) + float(clean_row['train/cls_loss']) + float(clean_row['train/l1_loss']),
                'val_loss': float(clean_row['val/giou_loss']) + float(clean_row['val/cls_loss']) + float(clean_row['val/l1_loss']),
                'mAP50': float(clean_row['metrics/mAP50(B)']),
                'mAP50_95': float(clean_row['metrics/mAP50-95(B)']),
                'precision': float(clean_row['metrics/precision(B)']),
                'recall': float(clean_row['metrics/recall(B)']),
            })
    return data

def extract_ms_detr() -> List[Dict]:
    """Extract MS-DETR training data from JSON."""
    json_path = RESULTS_DIR / "ms_detr_v2" / "results.json"

    data = []
    with open(json_path) as f:
        rows = json.load(f)  # Load as a JSON array
        for row in rows:
            data.append({
                'epoch': int(row['epoch']),
                'train_loss': float(row['train_loss']),
                'val_loss': None,
                'mAP50': float(row['mAP50']),
                'mAP50_95': float(row['mAP50-95']),
                'precision': None,
                'recall': None,
            })
    return data

def extract_rf_detr() -> List[Dict]:
    """Extract RF-DETR training data from JSONL log."""
    log_path = RESULTS_DIR / "rf_detr" / "log.txt"

    data = []
    with open(log_path) as f:
        for line in f:
            obj = json.loads(line)
            if 'epoch' in obj and 'test_results_json' in obj:
                test_results = obj['test_results_json']
                data.append({
                    'epoch': int(obj['epoch']) + 1,  # Convert 0-indexed to 1-indexed
                    'train_loss': float(obj['train_loss']),
                    'val_loss': float(obj.get('test_loss', 0)),
                    'mAP50': float(test_results['map']),
                    'mAP50_95': test_results['class_map'][1]['map@50:95'],  # 'all' class
                    'precision': float(test_results['precision']),
                    'recall': float(test_results['recall']),
                })
    return data

def save_training_data(name: str, data: List[Dict]):
    """Save extracted training data to CSV."""
    output_path = RESULTS_DIR / f"{name}_training_data.csv"

    if not data:
        print(f"No data extracted for {name}")
        return

    keys = data[0].keys()
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {name}: {len(data)} epochs to {output_path}")
    return output_path

if __name__ == "__main__":
    # Extract all models
    models = {
        'yolov12_single': lambda: extract_yolov12('YOLOv12-L (Single)', 'single'),
        'yolov12_ddp': lambda: extract_yolov12('YOLOv12-L (DDP)', 'ddp'),
        'so_detr': extract_so_detr,
        'ms_detr': extract_ms_detr,
        'rf_detr': extract_rf_detr,
    }

    for model_name, extract_fn in models.items():
        try:
            data = extract_fn()
            save_training_data(model_name, data)
        except Exception as e:
            print(f"Error extracting {model_name}: {e}")
            import traceback
            traceback.print_exc()
