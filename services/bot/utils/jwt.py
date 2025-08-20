import logging
from jose import JWTError, jwt
from config import settings

logger = logging.getLogger(__name__)

def get_token_payload(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        
        if payload is None:
            return None
        
        return payload

    except JWTError:
        return None
    
def validate_token(token: str) -> bool:
    try:
        payload = get_token_payload(token)
        return payload is not None
    except Exception as e:
        logger.error(f"Ошибка валидации токена {e}")
        return False
        