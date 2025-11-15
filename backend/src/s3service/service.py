import os.path
from enum import Enum
from pathlib import Path

from fastapi import UploadFile

from src.s3service.bucket import S3BucketUtil
from src.s3service.file_util.image import ImageUtil


class MediaSection(Enum):
    product = "product"
    profile = "profile"


class MediaService:
    def __init__(self, s3_util: S3BucketUtil, img_util: ImageUtil):
        self._s3_util = s3_util
        self._img_util = img_util

    async def save_image_s3(self, uploaded_file: UploadFile, section: MediaSection) -> str:
        file_path = await self._img_util.save_image(uploaded_file=uploaded_file)

        filename = Path(file_path).name

        key_path = f"images/{section.value}/{filename}"

        await self._s3_util.upload(key_path=key_path, filename=filename)
        await self._img_util.delete_image(file_path)
        return key_path

    async def get_image_s3(self, key_path: str) -> str:
        file_path = self._s3_util.tmp_storage / Path(key_path).name
        if await self._img_util.is_exist(file_path=file_path):
            return str(file_path)

        img_path: str = await self._s3_util.download(key_path=key_path)
        return img_path

    async def get_image_link(self, key_path: str) -> str:
        return await self._s3_util.get_download_link(key_path=key_path)

