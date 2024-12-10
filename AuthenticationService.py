from abc import ABC, abstractmethod
from fastapi import HTTPException


class AuthenticationService(ABC):
    @abstractmethod
    def is_valid_token(self, user_token: str) -> bool:
        pass

    @abstractmethod
    def get_user_id(self, user_token: str) -> int:
        pass


class StubAuthenticationService(AuthenticationService):
    def is_valid_token(self, user_token: str) -> bool:
        return user_token == "valid_token"

    def get_user_id(self, user_token: str) -> int:
        if user_token == "valid_token":
            return 1
        raise HTTPException(status_code=401, detail="Invalid token")
