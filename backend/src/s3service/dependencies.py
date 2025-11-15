from src.s3service.service import MediaService
from src.s3service.file_util.image import ImageUtil
from src.s3service.bucket import S3BucketUtil
from src.config import settings


def get_media_service() -> MediaService:
    s3_util = S3BucketUtil(bucket_name=settings.s3bucket.AWS_BUCKET_NAME,
                           region=settings.s3bucket.AWS_REGION,
                           secret_key=settings.s3bucket.AWS_SECRET_KEY,
                           access_key=settings.s3bucket.AWS_ACCESS_KEY,
                           tmp_storage=settings.s3bucket.media_storage)
    img_util = ImageUtil(upload_dir=settings.s3bucket.media_storage)
    service = MediaService(img_util=img_util, s3_util=s3_util)

    return service
