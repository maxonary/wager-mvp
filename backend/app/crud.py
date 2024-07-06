import requests
import os
from sqlalchemy.orm import Session
from . import models, schemas

API_URL = "https://api.clashroyale.com/v1"
API_KEY = os.getenv("API_KEY")

def get_battle_log(player_tag: str):
    headers = {
        'Authorization ': f'Bearer {API_KEY}'
    }
    response = requests.get(f'{API_URL}/players/{player_tag}/battlelog', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player_by_tag(db: Session, tag: str):
    return db.query(models.Player).filter(models.Player.tag == tag).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(tag=player.tag)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def create_bet(db: Session, bet: schemas.BetCreate):
    db_bet = models.Bet(**bet.dict())
    db.add(db_bet)
    db.commit()
    db.refresh(db_bet)
    return db_bet

def update_player_points(db: Session, player: schemas.Player, points: int):
    db_player = get_player_by_tag(db, player.tag)
    if db_player:
        db_player.points += points
        db.commit()
        db.refresh(db_player)
        return db_player
    return None

def get_leaderboard(db: Session, limit: int = 10):
    return db.query(models.Player).order_by(models.Player.points.desc()).limit(limit).all()