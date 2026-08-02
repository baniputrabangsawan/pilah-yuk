from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from src.classifier import (
    InvalidLabelsError,
    LabelsNotFoundError,
    ModelNotFoundError,
    get_input_size,
    load_labels,
    load_model,
    predict,
)


class ModelStub:
    input_shape = (None, 4, 5, 3)

    def predict(self, batch: np.ndarray, verbose: int) -> np.ndarray:
        assert batch.shape == (1, 4, 5, 3)
        assert verbose == 0
        return np.array([[0.1, 0.7, 0.2, 0.0]], dtype=np.float32)


def test_missing_files_raise_clear_errors(tmp_path: Path) -> None:
    with pytest.raises(ModelNotFoundError):
        load_model(tmp_path / "missing.h5")
    with pytest.raises(LabelsNotFoundError):
        load_labels(tmp_path / "missing.txt")


def test_load_labels_removes_numeric_prefix(tmp_path: Path) -> None:
    path = tmp_path / "labels.txt"
    path.write_text("0 cardboard\n1: Glass\n", encoding="utf-8")
    assert load_labels(path) == ["cardboard", "glass"]


def test_empty_labels_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "labels.txt"
    path.write_text("\n", encoding="utf-8")
    with pytest.raises(InvalidLabelsError):
        load_labels(path)


def test_detects_input_shape_and_ranks_top_three() -> None:
    model = ModelStub()
    assert get_input_size(model) == (4, 5)
    result = predict(
        model,
        ["cardboard", "glass", "metal", "paper"],
        Image.new("RGB", (2, 2)),
    )
    assert result.category == "glass"
    assert result.confidence == pytest.approx(0.7)
    assert [category for category, _ in result.top_predictions] == [
        "glass",
        "metal",
        "cardboard",
    ]


def test_rejects_label_output_mismatch() -> None:
    with pytest.raises(InvalidLabelsError):
        predict(ModelStub(), ["glass"], Image.new("RGB", (2, 2)))
