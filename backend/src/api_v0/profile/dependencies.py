from src.api_v0.profile.service import ProfileService, LikeService


def get_profile_service() -> ProfileService:
    return ProfileService()
def get_like_service()->LikeService:
    return LikeService()