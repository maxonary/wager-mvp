from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    userTag: str
    balance: int = 5
    username: Optional[str] = None
    wins: int = 0
    lastProcessedBattleTime: Optional[str] = None  # Initialize to None
