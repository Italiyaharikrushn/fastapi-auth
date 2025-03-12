from pydantic import BaseModel, validator
import enum

class RoleEnum(str, enum.Enum):  
    SELLER = "Seller"
    ADMIN = "Admin"
    CUSTOMER = "Customer"

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: str  
    password: str  
    phone: str
    gender: str
    role: RoleEnum = RoleEnum.CUSTOMER  # ✅ Default to "Customer", but can be changed

    @validator("role", pre=True, always=True)
    def validate_role(cls, value):
        if isinstance(value, str):
            value = value.title()  # ✅ Convert "admin" → "Admin"
            if value in RoleEnum._value2member_map_:
                return RoleEnum(value)
            raise ValueError(f"Invalid role: {value}. Allowed: {list(RoleEnum)}")
        return value

    class Config:
        orm_mode = True  
        use_enum_values = True  

class LoginSchema(BaseModel):
    email: str
    password: str