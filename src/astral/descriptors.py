from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .config import AstralConfig


Array = np.ndarray


@dataclass(frozen=True)
class DescriptorBundle:
    trend: Array
    residual: Array
    frequency: Array
    shape: Array
    analytic: Array


def _as_series(x: Array) -> Array:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2 or x.shape[1] < 2:
        raise ValueError("a series must have shape (channels, length>=2)")
    if not np.isfinite(x).all():
        raise ValueError("series contains nonfinite values")
    return x


def standardize_channels(x: Array, epsilon: float = 1.0e-6) -> Array:
    x = _as_series(x)
    mean = x.mean(axis=1, keepdims=True)
    scale = x.std(axis=1, keepdims=True)
    return (x - mean) / np.maximum(scale, epsilon)


def effective_odd_window(requested: int, length: int) -> int:
    if requested <= 0 or requested % 2 == 0:
        raise ValueError("requested window must be positive and odd")
    return min(requested, 2 * ((length - 1) // 2) + 1)


def moving_average(x: Array, window: int) -> Array:
    x = _as_series(x)
    w = effective_odd_window(window, x.shape[1])
    radius = w // 2
    padded = np.pad(x, ((0, 0), (radius, radius)), mode="edge")
    kernel = np.ones(w, dtype=np.float64) / w
    return np.stack([np.convolve(row, kernel, mode="valid") for row in padded])


def adaptive_average_pool(x: Array, output_size: int) -> Array:
    x = _as_series(x)
    length = x.shape[1]
    pooled = np.empty((x.shape[0], output_size), dtype=np.float64)
    for i in range(output_size):
        start = int(np.floor(i * length / output_size))
        stop = int(np.ceil((i + 1) * length / output_size))
        stop = max(stop, start + 1)
        pooled[:, i] = x[:, start:stop].mean(axis=1)
    return pooled


def first_difference(x: Array) -> Array:
    x = _as_series(x)
    return np.diff(x, axis=1)


def _acf(x: Array, lags: int) -> Array:
    values = []
    for lag in range(1, lags + 1):
        if lag >= x.shape[1]:
            values.append(np.zeros(x.shape[0], dtype=np.float64))
        else:
            values.append(np.mean(x[:, :-lag] * x[:, lag:], axis=1))
    return np.stack(values, axis=1) if values else np.empty((x.shape[0], 0))


def _frequency_descriptor(residual: Array, pool_length: int, epsilon: float) -> Array:
    amplitude = np.log1p(np.abs(np.fft.rfft(residual, axis=1)))
    norms = np.linalg.norm(amplitude, axis=1, keepdims=True)
    normalized = amplitude / np.maximum(norms, epsilon)
    return adaptive_average_pool(normalized, pool_length).reshape(-1)


def extract_descriptors(x: Array, config: AstralConfig | None = None) -> DescriptorBundle:
    cfg = config or AstralConfig()
    standardized_input = standardize_channels(x, cfg.epsilon)

    trend_parts = []
    residuals = {}
    for requested in cfg.windows:
        trend = moving_average(standardized_input, requested)
        residuals[requested] = standardized_input - trend
        ztrend = standardize_channels(trend, cfg.epsilon)
        trend_parts.append(adaptive_average_pool(ztrend, cfg.pool_length).reshape(-1))
        trend_parts.append(
            adaptive_average_pool(first_difference(ztrend), cfg.pool_length).reshape(-1)
        )
    trend_descriptor = np.concatenate(trend_parts)

    widest = max(cfg.windows)
    residual = standardize_channels(residuals[widest], cfg.epsilon)
    acf = _acf(residual, cfg.acf_lags)
    residual_descriptor = np.concatenate(
        [
            acf.reshape(-1),
            np.mean(np.abs(residual), axis=1),
            np.std(residual, axis=1),
            np.std(first_difference(residual), axis=1),
        ]
    )
    frequency_descriptor = _frequency_descriptor(
        residual, cfg.pool_length, cfg.epsilon
    )
    shape = adaptive_average_pool(standardized_input, cfg.pool_length).reshape(-1)
    analytic = np.concatenate(
        [trend_descriptor, residual_descriptor, frequency_descriptor, shape]
    )
    for name, value in {
        "trend": trend_descriptor,
        "residual": residual_descriptor,
        "frequency": frequency_descriptor,
        "shape": shape,
        "analytic": analytic,
    }.items():
        if not np.isfinite(value).all():
            raise FloatingPointError(f"{name} descriptor contains nonfinite values")
    return DescriptorBundle(
        trend=trend_descriptor,
        residual=residual_descriptor,
        frequency=frequency_descriptor,
        shape=shape,
        analytic=analytic,
    )


def extract_dataset(
    X: Iterable[Array], config: AstralConfig | None = None
) -> DescriptorBundle:
    bundles = [extract_descriptors(x, config) for x in X]
    if not bundles:
        raise ValueError("dataset is empty")
    return DescriptorBundle(
        trend=np.stack([b.trend for b in bundles]),
        residual=np.stack([b.residual for b in bundles]),
        frequency=np.stack([b.frequency for b in bundles]),
        shape=np.stack([b.shape for b in bundles]),
        analytic=np.stack([b.analytic for b in bundles]),
    )

