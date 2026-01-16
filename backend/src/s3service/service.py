import os.path
from enum import Enum
from io import BytesIO
from fastapi import UploadFile
from src.s3service.bucket import S3BucketUtil
from src.s3service.file_util.image import ImageUtil
import logging
logger = logging.getLogger(__name__)

class MediaSection(Enum):
    product = "product"
    profile = "profile"


class MediaService:
    def __init__(self, s3_util: S3BucketUtil, img_util: ImageUtil):
        self._s3_util = s3_util
        self._img_util = img_util

    async def save_image_s3(self, uploaded_file: UploadFile, section: MediaSection) -> str:
        content = await self._img_util.validate_image(uploaded_file)
        filename = uploaded_file.filename

        key_path = f"images/{section.value}/{filename}"

        await self._s3_util.upload(key_path=key_path, file_obj=BytesIO(content))
        logger.info("Image saved to S3")
        return key_path

    async def get_image_link(self, key_path: str) -> str:
        return await self._s3_util.get_download_link(key_path=key_path)

    logger.info("Image link fetched from S3")

    async def delete_image(self, key_path: str) -> None:
        await self._s3_util.delete_file(key_path)
        logger.info("Image deleted from S3")
