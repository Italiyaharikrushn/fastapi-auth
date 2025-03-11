from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db
import crud.base
from schemas.client import ClientCreate,ClientUpdate
from typing import List, Any
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user
from models.client import Client

router = APIRouter()

# create POST
@router.post("/create", status_code=201)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
):
    create_client = ClientCreate(
        first_name=client_in.first_name,
        last_name=client_in.last_name,
        email=client_in.email,
        phone=client_in.phone,
        gender=client_in.gender,
    )
    client = crud.client.create(db=db, obj_in=create_client)
    return client

# get all GET
@router.get("/get", status_code=200)
def get_all_clients(db: Session = Depends(get_db)):
    clients = crud.client.get(db=db)
    return clients

# get single GET
@router.get("/get/{client_id}", status_code=200)
def get_get_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.client.get_by_id(db=db, client_id=client_id)
    if client is None:
        return {"error": "Client not found"}
    return client

# delete data DELETE
@router.delete("/delete/{client_id}", status_code=200)
def delete_user(client_id: int, db: Session = Depends(dependencies.get_db)):
    result = crud.client.get(db=db, id=client_id)

    result.status = 0
    db.commit()

    return "User Deleted successfully"

# update data PUT
@router.put("/update/{client_id}", status_code=200)
def update_user(client_id: int, user_update: ClientUpdate, db: Session = Depends(get_db)):
    client = crud.client.get_by_id(db=db, client_id=client_id)
    
    updated_client = crud.client.update(db=db, db_obj=client, obj_in=user_update)
    return {"message": "User updated successfully", "user": updated_client}
