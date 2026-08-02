"""Local Keras model loading and prediction."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from src.utils import prepare_image_for_model

MODEL_PATH = Path("model/keras_model.h5")
LABELS_PATH = Path("model/labels.txt")


class ClassifierError(RuntimeError):
    """Base error for classifier failures."""


class ModelNotFoundError(ClassifierError):
    """Raised when the local model is unavailable."""


class LabelsNotFoundError(ClassifierError):
    """Raised when the label file is unavailable."""


class InvalidLabelsError(ClassifierError):
    """Raised when labels cannot represent model outputs."""


class IncompatibleModelError(ClassifierError):
    """Raised when model input or output is unsupported."""


@dataclass(frozen=True)
class Prediction:
    category: str
    confidence: float
    top_predictions: list[tuple[str, float]]


def load_labels(path: Path = LABELS_PATH) -> list[str]:
    if not path.is_file():
        raise LabelsNotFoundError(f"File label tidak ditemukan: {path}")

    labels = [
        re.sub(r"^\s*\d+\s*[:.)-]?\s*", "", line).strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not labels or any(not label for label in labels):
        raise InvalidLabelsError("File label kosong atau berisi label tidak valid.")
    if len(labels) != len(set(labels)):
        raise InvalidLabelsError("File label berisi kategori duplikat.")
    return labels


def load_model(path: Path = MODEL_PATH) -> Any:
    if not path.is_file():
        raise ModelNotFoundError(f"Model tidak ditemukan: {path}")
    try:
        from tensorflow.keras.models import load_model as keras_load_model

        return keras_load_model(path, compile=False)
    except Exception as exc:
        raise IncompatibleModelError(f"Model gagal dimuat: {exc}") from exc


def get_input_size(model: Any) -> tuple[int, int]:
    shape = model.input_shape
    if isinstance(shape, list):
        if len(shape) != 1:
            raise IncompatibleModelError("Model multi-input belum didukung.")
        shape = shape[0]
    if len(shape) != 4 or shape[3] != 3 or shape[1] is None or shape[2] is None:
        raise IncompatibleModelError(
            "Model harus memiliki input (batch, tinggi, lebar, 3)."
        )
    return int(shape[1]), int(shape[2])


def predict(model: Any, labels: list[str], image: Image.Image) -> Prediction:
    batch = prepare_image_for_model(image, get_input_size(model))
    try:
        scores = np.asarray(model.predict(batch, verbose=0), dtype=np.float32)
    except Exception as exc:
        raise ClassifierError(f"Inferensi model gagal: {exc}") from exc

    if scores.ndim != 2 or scores.shape[0] != 1:
        raise IncompatibleModelError("Output model harus berbentuk (1, jumlah_kelas).")
    values = scores[0]
    if len(values) != len(labels):
        raise InvalidLabelsError(
            f"Jumlah label ({len(labels)}) tidak sama dengan output model ({len(values)})."
        )
    if not np.all(np.isfinite(values)):
        raise IncompatibleModelError("Output model mengandung nilai yang tidak valid.")

    ranked = np.argsort(values)[::-1][:3]
    top = [(labels[index], float(values[index])) for index in ranked]
    return Prediction(top[0][0], top[0][1], top)
