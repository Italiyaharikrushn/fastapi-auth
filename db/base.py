# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base
from db.base_class import BaseDefault
from models.user import User
from models.client import Client
from models.product import Product