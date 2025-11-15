from src.api_v0.profile.service import ProfileService


def get_profile_service() -> ProfileService:
    return ProfileService()
