from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from schemas.user import UserDetails, UserOnly, UserCreate, UserInDBBase
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()

@router.get("", status_code=200)
def fetch_all_users(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all users
    """
    users = crud.user.get_all_user(db=db)
    return users

@router.get("/{user_id}", status_code=200)
def fetch_all_users(
    *,
    user_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch users by id
    """
    user = crud.user.get_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user

@router.delete("/{user_id}", status_code=200)
def delete_user(*, user_id: int, db: Session = Depends(dependencies.get_db)) -> dict:
    """
    Delete User
    """
    result = crud.user.get(db=db, id=user_id)
    result.status = 0
    db.commit()

    return "User Deleted successfully"
