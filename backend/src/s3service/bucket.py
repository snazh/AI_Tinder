import os
from pathlib import Path

import aioboto3
from botocore.exceptions import ClientError


class S3BucketUtil:

    def __init__(self, bucket_name: str, region: str,
                 access_key: str, secret_key: str,
                 tmp_storage: Path):
        self.bucket = bucket_name
        self._session = aioboto3.Session()
        self._client_params = {
            "service_name": "s3",
            "region_name": region,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        self.tmp_storage = tmp_storage

    async def upload(self, key_path: str, filename: str) -> None:

        async with self._session.client(**self._client_params) as s3:
            try:
                file_path = os.path.join(self.tmp_storage, filename)
                await s3.upload_file(file_path, self.bucket, key_path)
                # logger.info(f"✅ File uploaded successfully.")

            except Exception as e:
                # logger.error(f"❌ Upload failed: {e}")
                raise e

    async def download(self, key_path: str) -> str:
        filename = Path(key_path).name
        async with self._session.client(**self._client_params) as s3:
            try:
                download_path = os.path.join(self.tmp_storage, filename)
                with open(download_path, "wb") as f:
                    await s3.download_fileobj(self.bucket, key_path, f)
                return str(download_path)
            except Exception as e:
                # logger.error(f"❌ Download failed: {e}")
                raise e

    async def get_download_link(self, key_path: str) -> str:

        async with self._session.client(**self._client_params) as s3:
            try:
                url = await s3.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={
                        "Bucket": self.bucket,
                        "Key": key_path,
                    },
                    ExpiresIn=3600  # 1 hour
                )
                return url
            except Exception as e:
                # logger.error(f"Error getting file link {e}")
                raise e

    async def delete_file(self, key_path: str) -> None:
        async with self._session.client(**self._client_params) as s3:
            try:
                await s3.delete_object(Bucket=self.bucket, Key=key_path)
            except ClientError as e:
                # logger.error(f"❌ Error deleting file: {e}")
                raise e
