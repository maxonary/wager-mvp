from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/bets/", response_model=schemas.Bet)
def create_bet(bet: schemas.BetCreate, db: Session = Depends(get_db)):
    db_player1 = crud.get_player_by_tag(db, bet.player1_tag)
    db_player2 = crud.get_player_by_tag(db, bet.player2_tag)
    if not db_player1:
        db_player1 = crud.create_player(db, schemas.PlayerCreate(tag=bet.player1_tag))
    if not db_player2:
        db_player2 = crud.create_player(db, schemas.PlayerCreate(tag=bet.player2_tag))
    return crud.create_bet(db, bet)

@router.post("/bets/resolve/{bet_id}", response_model=schemas.Bet)
def resolve_bet(bet_id: int, winner_tag: str, db: Session = Depends(get_db)):
    bet = db.query(models.Bet).filter(models.Bet.id == bet_id).first()
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    bet.winner_tag = winner_tag
    if winner_tag == bet.player1_tag:
        winner = bet.player1_tag
        loser = bet.player2_tag
    else:
        winner = bet.player2_tag
        loser = bet.player1_tag
    crud.update_player_points(db, schemas.Player(tag=winner), bet.bet_amount)
    crud.update_player_points(db, schemas.Player(tag=loser), -bet.bet_amount)
    db.commit()
    db.refresh(bet)
    return bet