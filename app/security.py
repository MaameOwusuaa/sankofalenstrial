from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .models import User, Role
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer = HTTPBearer(auto_error=False)
ALGORITHM = 'HS256'

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user: User) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({'sub': str(user.id), 'role': user.role.value, 'exp': exp}, settings.secret_key, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials=Depends(bearer), db: Session=Depends(get_db)) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication required')
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[ALGORITHM])
        user_id = int(payload.get('sub'))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail='User is inactive or unavailable')
    return user

def require_roles(*roles: Role):

    def dependency(user: User=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail='Insufficient permissions')
        return user
    return dependency
