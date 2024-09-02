from pydantic import BaseModel

class Transaction(BaseModel):
    username: str
    time: str
    amount: float