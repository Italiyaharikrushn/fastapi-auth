from fastapi import APIRouter, Depends, status, HTTPException
from api.dependencies import get_db
from core.security import verify_password
from schemas.auth import LoginSchema, RegisterSchema
from sqlalchemy.orm import Session
from services.user_service import create_access_token, create_user, get_user_by_email
from core.config import settings
from models.user import User

router = APIRouter()

@router.post('/register', response_model=RegisterSchema, response_model_exclude={'password'}, status_code=(status.HTTP_201_CREATED))
def register(register_schema: RegisterSchema, db: Session = Depends(get_db)):
    existing_users = get_user_by_email(db, register_schema.email)
    if existing_users:
        raise HTTPException(status_code=(status.HTTP_409_CONFLICT),
                            detail='Email already exists')
    user = create_user(db, register_schema)
    return user

@router.post('/login', status_code=status.HTTP_200_OK)
def login(login_schema: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_schema.email).first()  # ✅ Now User is recognized
    
    if not user or not verify_password(login_schema.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(claim={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
