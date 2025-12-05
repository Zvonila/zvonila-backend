from src.auth.utils import PasswordService, JWTService
from src.config import settings

def get_password_service() -> PasswordService:
    return PasswordService()

def get_jwt_service() -> JWTService:
    return JWTService(
        private_key_path=settings.PRIVATE_KEY_PATH,
        public_key_path=settings.PUBLIC_KEY_PATH
    )