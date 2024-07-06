from fastapi import FastAPI
from app.api.endpoints import bets, leaderboard
from app.database import engine
import app.models as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(bets.router, prefix="/api/v1")
app.include_router(leaderboard.router, prefix="/api/v1")