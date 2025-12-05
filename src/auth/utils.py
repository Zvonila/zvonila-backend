from argon2 import PasswordHasher, exceptions as argon_exceptions
from jwt import JWT, jwk_from_pem
from typing import Any, Dict
from pathlib import Path

KEY_ALG = 'RS256'


class PasswordService:
    """Сервис для хэширования и проверки паролей"""

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash(self, raw_password: str) -> str:
        """Возвращает Argon2-хэш пароля"""
        return self._hasher.hash(raw_password)

    def verify(self, hash_password: str, raw_password: str) -> bool:
        """Проверяет пароль, возвращает True/False без выброса исключений"""
        try:
            self._hasher.verify(hash_password, raw_password)
            return True
        except argon_exceptions.VerifyMismatchError:
            return False


class JWTService:
    """Сервис для генерации и валидации JWT токенов"""

    def __init__(
            self, 
            private_key_path: str,
            public_key_path: str,
            key_alg: str = KEY_ALG,
        ) -> None:
        self._jwt = JWT()
        self._alg = key_alg
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def generate(self, private_claims: Dict[str, Any]) -> str:
        """Создает JWT, подписанный приватным ключом"""
        key = self._load_key(self.private_key_path)
        return self._jwt.encode(private_claims, key, alg=self._alg)

    def decode(self, token: str) -> Dict[str, Any]:
        """Декодирует и проверяет JWT по публичному ключу"""
        key = self._load_key(self.public_key_path)
        return self._jwt.decode(token, key, do_time_check=True)

    @staticmethod
    def _load_key(path: str):
        with Path(path).open("rb") as f:
            return jwk_from_pem(f.read())