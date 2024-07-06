from pydantic import BaseModel

class PlayerBase(BaseModel):
    tag: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    points: int

    class Config:
        orm_mode = True

class BetBase(BaseModel):
    player1_tag: str
    player2_tag: str
    bet_amount: float

class BetCreate(BetBase):
    pass

class Bet(BetBase):
    id: int
    winner_tag: str

    class Config:
        orm_mode = True