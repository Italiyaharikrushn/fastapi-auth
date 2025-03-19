from db.database import SessionLocal
from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from jose import JWTError, jwt
from datetime import datetime, timedelta

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request):
    return request.state.current_user

def get_current_seller(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if user and user.role == "seller":
        return user.id
    else:
        raise HTTPException(status_code=400, detail="User is not a seller")
