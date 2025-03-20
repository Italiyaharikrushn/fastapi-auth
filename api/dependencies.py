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

# Ensure current user is a seller
def get_current_user(request: Request):
    return request.state.current_user
