from pathlib import Path
from botocore.client import Config
import logging
import aioboto3
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class S3BucketUtil:

    def __init__(self, bucket: str, endpoint_url: str,
                 access_key: str, secret_key: str,
                 tmp_storage: Path):
        self.bucket = bucket
        self._session = aioboto3.Session()
        self._client_params = {
            "service_name": "s3",
            "endpoint_url": endpoint_url,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "config": Config(signature_version="s3v4")

        }
        self.tmp_storage = tmp_storage

    async def upload(self, key_path: str, file_obj) -> None:
        async with self._session.client(**self._client_params) as s3:
            await s3.upload_fileobj(file_obj, self.bucket, key_path)

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
                logger.error(f"Error getting file link {e}")
                raise

    async def delete_file(self, key_path: str) -> None:
        async with self._session.client(**self._client_params) as s3:
            try:
                await s3.delete_object(Bucket=self.bucket, Key=key_path)
            except ClientError as e:
                logger.error(f"Error deleting file: {e}")
                raise
