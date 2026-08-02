from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from src.utils import InvalidImageError, load_image, prepare_image_for_model


def image_bytes(format_: str, mode: str = "RGB") -> bytes:
    output = BytesIO()
    Image.new(mode, (8, 6), 128).save(output, format=format_)
    return output.getvalue()


@pytest.mark.parametrize("format_", ["JPEG", "PNG"])
def test_loads_supported_images(format_: str) -> None:
    image = load_image(image_bytes(format_))
    assert image.mode == "RGB"
    assert image.size == (8, 6)


@pytest.mark.parametrize("mode", ["RGBA", "L"])
def test_converts_image_to_rgb(mode: str) -> None:
    assert load_image(image_bytes("PNG", mode)).mode == "RGB"


@pytest.mark.parametrize("data", [b"not an image", b""])
def test_rejects_invalid_files(data: bytes) -> None:
    with pytest.raises(InvalidImageError):
        load_image(data)


def test_prepares_float32_normalized_batch() -> None:
    batch = prepare_image_for_model(Image.new("RGB", (4, 4), (0, 127, 255)), (6, 8))
    assert batch.shape == (1, 6, 8, 3)
    assert batch.dtype == np.float32
    assert -1.0 <= batch.min() <= batch.max() <= 1.0
