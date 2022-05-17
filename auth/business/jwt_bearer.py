from typing import Tuple

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.business.jwt_handler import decode_jwt


def verify_jwt(jwtoken: str) -> Tuple[bool, dict]:
    is_token_valid: bool = False
    payload = decode_jwt(jwtoken)
    if payload:
        is_token_valid = True
    return is_token_valid, payload


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication token")

            is_token_valid, payload = verify_jwt(credentials.credentials)
            if not is_token_valid:
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token")
