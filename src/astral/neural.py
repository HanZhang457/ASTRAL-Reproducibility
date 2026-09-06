"""Optional PyTorch realization of the ASTRAL relation geometry.

This module is imported only when the neural dependency set is installed.
"""

from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class ConvBranch(nn.Module):
    def __init__(self, in_channels: int, branch_dim: int = 32) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(in_channels, 64, 7, padding=3),
            nn.GELU(),
            nn.Conv1d(64, 64, 5, padding=2),
            nn.GELU(),
            nn.Conv1d(64, branch_dim, 3, padding=1),
            nn.AdaptiveAvgPool1d(1),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.net(x).squeeze(-1)


class AstralNeuralEncoder(nn.Module):
    def __init__(
        self,
        channels: int,
        windows: int = 3,
        branch_dim: int = 32,
        output_dim: int = 96,
        confidence_floor: float = 0.02,
    ) -> None:
        super().__init__()
        self.trend = ConvBranch(channels * windows, branch_dim)
        self.residual = ConvBranch(channels, branch_dim)
        self.frequency = ConvBranch(channels, branch_dim)
        self.gate = nn.Sequential(
            nn.Linear(3 * branch_dim, branch_dim),
            nn.GELU(),
            nn.Linear(branch_dim, 3),
        )
        self.projector = nn.Linear(3 * branch_dim, output_dim)
        self.confidence_floor = confidence_floor

    @staticmethod
    def spectral_confidence(spectrum: Tensor, eps: float = 1.0e-8) -> Tensor:
        nonnegative = spectrum.abs().flatten(1)
        p = nonnegative / nonnegative.sum(dim=1, keepdim=True).clamp_min(eps)
        entropy = -(p * (p + eps).log()).sum(dim=1)
        return 1.0 - entropy / math.log(max(p.shape[1], 2))

    def forward(
        self, trend_stack: Tensor, residual: Tensor, spectrum: Tensor
    ) -> dict[str, Tensor]:
        e_t = self.trend(trend_stack)
        e_r = self.residual(residual)
        e_f = self.frequency(spectrum)
        concatenated = torch.cat([e_t, e_r, e_f], dim=1)
        gate_logits = self.gate(concatenated)
        confidence = self.spectral_confidence(spectrum)
        gate_logits = gate_logits + torch.stack(
            [
                torch.zeros_like(confidence),
                torch.zeros_like(confidence),
                torch.log(confidence.clamp_min(0) + self.confidence_floor),
            ],
            dim=1,
        )
        gates = gate_logits.softmax(dim=1)
        gated = torch.cat(
            [
                gates[:, 0:1] * e_t,
                gates[:, 1:2] * e_r,
                gates[:, 2:3] * e_f,
            ],
            dim=1,
        )
        return {
            "z": self.projector(gated),
            "trend": e_t,
            "residual": e_r,
            "frequency": e_f,
            "gates": gates,
        }


def shifted_cosine(x: Tensor, y: Tensor) -> Tensor:
    return 0.5 * (1.0 + F.cosine_similarity(x, y, dim=-1))


def smooth_l1_relation(predicted: Tensor, target: Tensor) -> Tensor:
    return F.smooth_l1_loss(predicted, target)


def reliable_order_loss(
    similarity_ij: Tensor,
    similarity_il: Tensor,
    teacher_ij: Tensor,
    teacher_il: Tensor,
    margin: float = 0.05,
    temperature: float = 0.1,
) -> Tensor:
    reliable = (teacher_ij - teacher_il).abs() >= margin
    if not torch.any(reliable):
        return similarity_ij.sum() * 0.0
    sign = torch.sign(teacher_ij[reliable] - teacher_il[reliable])
    delta = similarity_ij[reliable] - similarity_il[reliable]
    return F.softplus(-sign * delta / temperature).mean()


def astral_objective(
    pair: Tensor,
    gram: Tensor,
    neighborhood: Tensor,
    branch: Tensor,
    order: Tensor,
) -> Tensor:
    return pair + 0.5 * gram + 0.25 * neighborhood + 0.5 * branch + 0.5 * order

