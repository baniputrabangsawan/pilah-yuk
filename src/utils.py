"""Image validation and preprocessing utilities."""

from __future__ import annotations

from io import BytesIO
from typing import BinaryIO

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000
SUPPORTED_FORMATS = {"JPEG", "PNG"}


class InvalidImageError(ValueError):
    """Raised when an uploaded image cannot be processed safely."""


def load_image(source: bytes | BinaryIO) -> Image.Image:
    """Load a JPEG or PNG as an RGB image without writing it to disk."""
    try:
        data = source if isinstance(source, bytes) else source.read()
    except (AttributeError, OSError) as exc:
        raise InvalidImageError("Gambar tidak dapat dibaca.") from exc

    if not data:
        raise InvalidImageError("File gambar kosong.")
    if len(data) > MAX_FILE_SIZE:
        raise InvalidImageError("Ukuran gambar melebihi batas 10 MB.")

    try:
        with Image.open(BytesIO(data)) as image:
            if image.format not in SUPPORTED_FORMATS:
                raise InvalidImageError("Format gambar harus JPEG atau PNG.")
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise InvalidImageError("Resolusi gambar terlalu besar.")
            image.load()
            return ImageOps.exif_transpose(image).convert("RGB")
    except (UnidentifiedImageError, OSError, SyntaxError) as exc:
        raise InvalidImageError("File bukan gambar JPEG/PNG yang valid.") from exc


def prepare_image_for_model(
    image: Image.Image, target_size: tuple[int, int]
) -> np.ndarray:
    """Resize and normalize an image into a Teachable Machine input batch."""
    height, width = target_size
    if height <= 0 or width <= 0:
        raise ValueError("Ukuran input model harus bernilai positif.")

    resized = image.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.asarray(resized, dtype=np.float32)
    return np.expand_dims((pixels / 127.5) - 1.0, axis=0)
