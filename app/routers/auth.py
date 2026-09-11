from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Passport, Role
from ..schemas import UserCreate, UserOut, LoginRequest, Token
from ..security import hash_password, verify_password, create_access_token, get_current_user
router = APIRouter(prefix='/api/auth', tags=['Authentication'])

@router.post('/register', response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session=Depends(get_db)):
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(409, 'Email already registered')
    user = User(first_name=payload.first_name, last_name=payload.last_name, email=payload.email.lower(), hashed_password=hash_password(payload.password), role=Role.user)
    db.add(user)
    db.flush()
    db.add(Passport(user_id=user.id))
    db.commit()
    db.refresh(user)
    return user

@router.post('/login', response_model=Token)
def login(payload: LoginRequest, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, 'Invalid email or password')
    return {'access_token': create_access_token(user), 'token_type': 'bearer'}

@router.get('/me', response_model=UserOut)
def me(user: User=Depends(get_current_user)):
    return user
