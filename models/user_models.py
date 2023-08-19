from beanie import Document, Indexed
from typing import Union, Optional

from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] | None = None
    disabled: bool = Field(default = False)
    scope: str = Field(default = "user")
    
class User_Register(BaseModel):
    username: str
    email: str
    password: str

class User_MongoDB(Document):
    username: Indexed(str, unique=True)    
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    disabled: bool = False
    scope: str = Field(default = "user")
    
    class Settings:
        name = "users"
    