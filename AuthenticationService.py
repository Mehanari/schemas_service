from abc import ABC, abstractmethod
from fastapi import HTTPException
import requests

AUTH_SERVICE_URL = "http://localhost:8001/exchange-token"


class AuthenticationService(ABC):
    @abstractmethod
    def get_user_id(self, user_token: str) -> int:
        pass


class StubAuthenticationService(AuthenticationService):
    def get_user_id(self, user_token: str) -> int:
        if user_token == "valid_token":
            return 1
        raise HTTPException(status_code=401, detail="Invalid token")


# Implementation of the abstract class
class AuthenticationServiceImpl(AuthenticationService):
    def get_user_id(self, user_token: str) -> int:
        headers = {"Authorization": f"Bearer {user_token}"}
        try:
            response = requests.get(AUTH_SERVICE_URL, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data["userId"]
            else:
                raise HTTPException(status_code=response.status_code,
                                    detail=response.json().get("detail", "Unknown error"))
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to authentication service: {e}")
