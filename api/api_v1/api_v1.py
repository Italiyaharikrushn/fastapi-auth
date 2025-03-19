from fastapi import APIRouter
from .endpoints import auth , user, product
route_v1 = APIRouter()
route_v1.include_router((auth.router), prefix='/auth', tags=['auth'])
route_v1.include_router((user.router), prefix='/user', tags=['user'])
route_v1.include_router((product.router), prefix='/product', tags=['product'])

