from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    userTag: str
    balance: int = 10
    username: Optional[str] = None
    wins: int = 0
