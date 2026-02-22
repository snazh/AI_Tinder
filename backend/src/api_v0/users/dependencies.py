from src.api_v0.users.service import UserService


def get_user_service() -> UserService:
    return UserService()
