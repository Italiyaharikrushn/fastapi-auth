from fastapi import APIRouter, Depends, status, HTTPException
from api.dependencies import get_db
from core.security import verify_password, get_password_hash
from schemas.auth import LoginSchema, RegisterSchema, RoleEnum
from sqlalchemy.orm import Session
from services.user_service import create_access_token, get_user_by_email
from core.config import settings
from datetime import datetime, timedelta
from models.user import User

router = APIRouter()

@router.post('/register')
def register(register_schema: RegisterSchema, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, register_schema.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        first_name=register_schema.first_name,
        last_name=register_schema.last_name,
        email=register_schema.email,
        password=get_password_hash(register_schema.password),
        phone=register_schema.phone,
        gender=register_schema.gender,
        role=register_schema.role,
        is_super_admin=False,
        expiry_date=datetime.utcnow() + timedelta(days=365)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/login', status_code=status.HTTP_200_OK)
def login(login_schema: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_schema.email).first()
    
    if not user or not verify_password(login_schema.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(claim={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
