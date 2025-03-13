from pydantic import BaseModel, validator, field_validator
import enum

class RoleEnum(str, enum.Enum):  
    SELLER = "SELLER"
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class RegisterSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    gender: str
    role: RoleEnum

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value):
        if isinstance(value, str):
            value = value.upper()
            if value not in RoleEnum._value2member_map_:
                raise ValueError(f"Invalid role: {value}. Allowed: {list(RoleEnum._value2member_map_.keys())}")
            return RoleEnum(value)
        return value

class LoginSchema(BaseModel):
    email: str
    password: str