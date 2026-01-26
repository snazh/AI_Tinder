from src.services.s3service.service import MediaService
from src.services.s3service.file_util.image import ImageUtil
from src.services.s3service.bucket import S3BucketUtil
from src.config import settings

def get_media_service() -> MediaService:
    s3_util = S3BucketUtil(bucket=settings.s3.S3_BUCKET,
                           endpoint_url=settings.s3.s3_endpoint,
                           secret_key=settings.s3.S3_SECRET_KEY,
                           access_key=settings.s3.S3_ACCESS_KEY,
                           tmp_storage=settings.s3.media_storage)
    img_util = ImageUtil()
    service = MediaService(img_util=img_util, s3_util=s3_util)

    return service
