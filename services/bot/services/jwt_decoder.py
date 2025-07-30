from jose import JWTError, jwt
from config import settings

def get_token_payload(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        
        if payload is None:
            return None
        
        return payload

    except JWTError:
        return None