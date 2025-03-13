from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt

from models.user import User
from core.security import get_password_hash
from core.config import settings
from schemas.auth import RegisterSchema

PREFIX = "Bearer"

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, register_schema: RegisterSchema):
    password_hash = get_password_hash(register_schema.password)
    expiry_date = datetime.utcnow() + timedelta(days=90)
    
    user = User(
        first_name=register_schema.first_name,
        last_name=register_schema.last_name,
        password=password_hash,
        email=register_schema.email,
        phone=register_schema.phone,
        gender=register_schema.gender,
        expiry_date=expiry_date,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(claim: dict, expires_delta: Optional[timedelta] = None):
    to_encode = claim.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60))
    to_encode.update({"exp": expire})
    
    jwt_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_token

def decode_access_token(token):
    try:
        auth_token = get_token(token)
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        print("Problem with token decode =>", str(e))
        return None

def get_token(header):
    bearer, _, token = header.partition(" ")
    if bearer != PREFIX:
        raise ValueError("Invalid token format")
    return token

def get_user_by_email_active(db: Session, email: str):
    return db.query(User).filter(User.email == email).all()