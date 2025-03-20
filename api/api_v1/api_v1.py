from fastapi import APIRouter
from .endpoints import auth , user, product, order, cart, shipping_address, billing_address
route_v1 = APIRouter()
route_v1.include_router((auth.router), prefix='/auth', tags=['auth'])
route_v1.include_router((user.router), prefix='/user', tags=['user'])
route_v1.include_router((product.router), prefix='/product', tags=['product'])
route_v1.include_router(order.router, prefix="/orders", tags=["Orders"])
route_v1.include_router(cart.router, prefix="/cart", tags=["Cart"])
route_v1.include_router(shipping_address.router, prefix="/shipping-address", tags=["Shipping Address"])
route_v1.include_router(billing_address.router, prefix="/billing-address", tags=["Billing Address"])