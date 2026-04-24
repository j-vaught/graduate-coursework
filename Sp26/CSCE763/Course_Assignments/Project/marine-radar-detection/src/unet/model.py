"""U-Net segmentation model for marine radar detection."""

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from tqdm import tqdm

from .utils import binary_mask_to_bboxes


class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.conv(x)


class UNet(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 1):
        super().__init__()

        channels = [64, 128, 256, 512, 1024]

        # Encoder
        self.enc1 = DoubleConv(in_channels, channels[0])
        self.enc2 = DoubleConv(channels[0], channels[1])
        self.enc3 = DoubleConv(channels[1], channels[2])
        self.enc4 = DoubleConv(channels[2], channels[3])

        self.bottleneck = DoubleConv(channels[3], channels[4])

        self.pool = nn.MaxPool2d(2)

        # Decoder
        self.up4 = nn.ConvTranspose2d(channels[4], channels[3], 2, stride=2)
        self.dec4 = DoubleConv(channels[4], channels[3])
        self.up3 = nn.ConvTranspose2d(channels[3], channels[2], 2, stride=2)
        self.dec3 = DoubleConv(channels[3], channels[2])
        self.up2 = nn.ConvTranspose2d(channels[2], channels[1], 2, stride=2)
        self.dec2 = DoubleConv(channels[2], channels[1])
        self.up1 = nn.ConvTranspose2d(channels[1], channels[0], 2, stride=2)
        self.dec1 = DoubleConv(channels[1], channels[0])

        self.out_conv = nn.Conv2d(channels[0], num_classes, 1)

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))

        b = self.bottleneck(self.pool(e4))

        # Decoder with skip connections
        d4 = self.up4(b)
        d4 = self.dec4(torch.cat([d4, e4], dim=1))
        d3 = self.up3(d4)
        d3 = self.dec3(torch.cat([d3, e3], dim=1))
        d2 = self.up2(d3)
        d2 = self.dec2(torch.cat([d2, e2], dim=1))
        d1 = self.up1(d2)
        d1 = self.dec1(torch.cat([d1, e1], dim=1))

        return self.out_conv(d1)


class DiceBCELoss(nn.Module):
    def __init__(self, dice_weight: float = 0.5, bce_weight: float = 0.5):
        super().__init__()
        self.dice_weight = dice_weight
        self.bce_weight = bce_weight

    def forward(self, pred, target):
        pred_sig = torch.sigmoid(pred)

        # Dice
        smooth = 1.0
        pred_flat = pred_sig.view(-1)
        target_flat = target.view(-1)
        intersection = (pred_flat * target_flat).sum()
        dice = 1 - (2.0 * intersection + smooth) / (pred_flat.sum() + target_flat.sum() + smooth)

        # BCE
        bce = F.binary_cross_entropy_with_logits(pred, target)

        return self.dice_weight * dice + self.bce_weight * bce


def train_unet(
    model: UNet,
    train_loader: DataLoader,
    val_loader: DataLoader,
    cfg: dict,
    output_dir: str | Path,
    seed: int = 42,
):
    """Train U-Net segmentation model."""
    torch.manual_seed(seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_cfg = cfg["training"]
    loss_cfg = cfg["loss"]
    device = torch.device(f"cuda:{train_cfg['device']}" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = DiceBCELoss(
        dice_weight=loss_cfg["dice_weight"],
        bce_weight=loss_cfg["bce_weight"],
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=train_cfg["lr"],
        weight_decay=train_cfg["weight_decay"],
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=train_cfg["T_max"])

    best_loss = float("inf")

    for epoch in range(train_cfg["epochs"]):
        model.train()
        epoch_loss = 0.0

        pbar = tqdm(train_loader, desc=f"Epoch {epoch + 1}/{train_cfg['epochs']}")
        for images, masks in pbar:
            images = images.to(device)
            masks = masks.to(device)

            pred = model(images)
            loss = criterion(pred, masks)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            pbar.set_postfix(loss=loss.item())

        scheduler.step()
        avg_loss = epoch_loss / len(train_loader)

        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), output_dir / f"best_seed{seed}.pth")

    return model


def predict_unet(
    model: UNet,
    image: torch.Tensor,
    device: str = "cuda:0",
    threshold: float = 0.5,
    min_area: int = 15,
) -> tuple[np.ndarray, np.ndarray]:
    """Run U-Net inference and extract bounding boxes from predicted mask.

    Returns:
        Tuple of (bboxes, predicted_mask).
    """
    model.eval()
    model.to(device)

    with torch.no_grad():
        pred = model(image.unsqueeze(0).to(device))
        pred_mask = (torch.sigmoid(pred) > threshold).squeeze().cpu().numpy().astype(np.uint8)

    bboxes = binary_mask_to_bboxes(pred_mask, min_area=min_area)
    return bboxes, pred_mask
