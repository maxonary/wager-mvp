# app/models/matchModel.py
from pydantic import BaseModel
from typing import Optional

class Match(BaseModel):
    matchID: Optional[str] = None
    userTag1: str
    userTag2: str
    winnerUserID: Optional[str] = None
    betAmount: int
    checked: bool = False
