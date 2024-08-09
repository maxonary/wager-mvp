# app/models/matchModel.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class Match(BaseModel):
    matchID: Optional[str] = None
    userTag1: str
    userTag2: str
    winnerUserID: Optional[str] = None
    betAmount: int
    checked: bool = False
    createdTime: datetime = datetime.now(timezone.utc)  # Use timezone-aware UTC datetime
    checkedTime: Optional[datetime] = None  # Set when the match is checked
