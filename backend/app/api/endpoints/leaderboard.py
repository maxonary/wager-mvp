from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leaderboard/", response_model=list[schemas.Player])
def read_leaderboard(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    players = crud.get_leaderboard(db, limit=limit)
    return players