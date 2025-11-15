from pathlib import Path
from fastapi import UploadFile
import uuid
import aiofiles.os


class FileUtil:

    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, content: bytes, original_filename: str) -> str:

        ext = Path(original_filename).suffix
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = self.upload_dir / unique_name
        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(content)

        return str(file_path)

    async def delete_file(self, file_path: str) -> None:
        path = Path(file_path)
        if not path.is_absolute():
            path = self.upload_dir / path

        if not path.exists():
            raise FileNotFoundError("File not found.")

        await aiofiles.os.remove(str(path))

    async def is_exist(self, file_path) -> bool:
        return await aiofiles.os.path.exists(file_path)
