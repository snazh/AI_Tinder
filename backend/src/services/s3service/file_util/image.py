from pathlib import Path

from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class ImageUtil:
    valid_ext = ["image/jpeg", "image/png", "image/webp"]

    async def validate_image(self, uploaded_file: UploadFile):

        if uploaded_file.content_type not in self.valid_ext:
            logger.error("Only JPG, PNG and WebP images allowed")
            raise
        content = await uploaded_file.read()
        try:
            image = Image.open(BytesIO(content))
            image.verify()
        except UnidentifiedImageError:
            logger.warning("Invalid image file uploaded")
            raise
        return content
