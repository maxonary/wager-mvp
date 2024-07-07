from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
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
def create_bet(bet: schemas.BetCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_player1 = crud.get_player_by_tag(db, bet.player1_tag)
    db_player2 = crud.get_player_by_tag(db, bet.player2_tag)
    if not db_player1:
        db_player1 = crud.create_player(db, schemas.PlayerCreate(tag=bet.player1_tag))
    if not db_player2:
        db_player2 = crud.create_player(db, schemas.PlayerCreate(tag=bet.player2_tag))
    bet = crud.create_bet(db, bet)
    background_tasks.add_task(crud.check_for_completed_game, bet.id, db)
    return bet

@router.post("/bets/resolve/{bet_id}", response_model=schemas.Bet)
def resolve_bet(bet_id: int, winner_tag: str, db: Session = Depends(get_db)):
    bet = crud.resolve_bet(bet_id, winner_tag, db)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return bet

@router.get("/battlelog/{player_tag}", response_model=dict)
def get_battle_log(player_tag: str):
    battle_log = crud.get_battle_log(player_tag)
    if not battle_log:
        raise HTTPException(status_code=404, detail="Battle log not found")
    return battle_log