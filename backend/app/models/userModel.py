from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    userTag: str
    email: EmailStr
    password: str  # This will store the hashed password
    balance: float
    username: Optional[str] = None
    wins: int = 0
    lastProcessedBattleTime: Optional[str] = None

class CreateUserRequest(BaseModel):
    userTag: str
    email: EmailStr
    password: str