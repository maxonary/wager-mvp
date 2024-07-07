import requests
import os
import time
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

def resolve_bet(bet_id: int, winner_tag: str, db: Session):
    bet = db.query(models.Bet).filter(models.Bet.id == bet_id).first()
    if not bet:
        return None
    bet.winner_tag = winner_tag
    if winner_tag == bet.player1_tag:
        winner = bet.player1_tag
        loser = bet.player2_tag
    else:
        winner = bet.player2_tag
        loser = bet.player1_tag
    update_player_points(db, schemas.Player(tag=winner), bet.bet_amount)
    update_player_points(db, schemas.Player(tag=loser), -bet.bet_amount)
    db.commit()
    db.refresh(bet)
    return bet

def check_for_completed_game(bet_id: int, db: Session):
    bet = db.query(models.Bet).filter(models.Bet.id == bet_id).first()
    if not bet:
        return None
    
    while True:
        battle_log1 = get_battle_log(bet.player1_tag)
        battle_log2 = get_battle_log(bet.player2_tag)
        if not battle_log1 or not battle_log2:
            continue

        # Check if there is a game between the two players
        for battle1 in battle_log1:
            for battle2 in battle_log2:
                if (battle1['battleTime'] == battle2['battleTime'] and
                    bet.player1_tag in [player['tag'] for player in battle1['team']] and
                    bet.player2_tag in [player['tag'] for player in battle2['team']]):
                    
                    # Determine the winner
                    crowns1 = next(player['crowns'] for player in battle1['team'] if player['tag'] == bet.player1_tag)
                    crowns2 = next(player['crowns'] for player in battle2['team'] if player['tag'] == bet.player2_tag)
                    
                    if crowns1 > crowns2:
                        winner_tag = bet.player1_tag
                    else:
                        winner_tag = bet.player2_tag
                    
                    resolve_bet(bet_id, winner_tag, db)
                    return

        time.sleep(60)  # Wait for 1 minute before checking again