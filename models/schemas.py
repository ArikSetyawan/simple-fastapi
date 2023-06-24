from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str
    photo: Optional[str] = None


class UserUpdate(BaseModel):
    id: int
    password: Optional[str] = None
    photo: Optional[str] = None