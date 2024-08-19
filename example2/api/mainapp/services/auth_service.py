import os
from fastapi import HTTPException

class AuthService:
    def authorize(self, auth_key: str):
        """
        Checks whether the request is authorized. If not an HttpResponseForbidden exceptionis raised

        Args:
            auth_key: The received http request
        """
        try:
            auth_key_env = os.getenv("AUTH_KEY")
            if auth_key == "":
                raise HTTPException(status_code=401)
            if auth_key != auth_key_env:
                raise HTTPException(status_code=401)
        except:
            raise HTTPException(status_code=401)