from sqlalchemy.orm import Session
from . import models, schemas

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