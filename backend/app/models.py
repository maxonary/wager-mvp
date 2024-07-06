from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, unique=True, index=True)
    points = Column(Integer, default=100)

class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True, index=True)
    player1_tag = Column(String)
    player2_tag = Column(String)
    bet_amount = Column(Float)
    winner_tag = Column(String, nullable=True)