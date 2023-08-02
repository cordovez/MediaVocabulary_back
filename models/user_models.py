from beanie import Document
from typing import Union, Optional

from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: Optional[str] | None = None
    disabled: bool | None = None
    
class User_MongoDB(Document):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None