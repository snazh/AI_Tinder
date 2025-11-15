from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile
from io import BytesIO
from src.api_v0.common.errors import BaseAppException
from src.s3service.file_util.base import FileUtil


class ImageError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(400, message)


class ImageUtil(FileUtil):

    async def save_image(self, uploaded_file: UploadFile) -> str:
        if uploaded_file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise ImageError(message="Only JPG, PNG and WebP images allowed")

        content = await uploaded_file.read()

        try:
            image = Image.open(BytesIO(content))
            image.verify()
        except UnidentifiedImageError:
            raise ImageError(message="Invalid image")
        return await super().save_file(content=content, original_filename=uploaded_file.filename)

    async def delete_image(self, file_path) -> None:
        await super().delete_file(file_path=file_path)
