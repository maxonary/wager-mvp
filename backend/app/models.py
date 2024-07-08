from pydantic import BaseModel

class BattleLogRequest(BaseModel):
    username: str
    opponent: str

class BattleLogResponse(BaseModel):
    winner: str