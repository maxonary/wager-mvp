from fastapi import FastAPI
from app.api.endpoints import getIP
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import getData
from app.api.endpoints import createUser
from app.api.endpoints import createMatch
from app.api.endpoints import getMatchResult
from app.api.endpoints import getLeaderBoard
from app.api.endpoints import increaseBalance

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(getData.router, prefix="/api/v1")

app.include_router(getIP.router, prefix="/api/v1")
app.include_router(createUser.router, prefix="/api/v1")
app.include_router(createMatch.router, prefix="/api/v1")
app.include_router(getMatchResult.router, prefix="/api/v1")
app.include_router(getLeaderBoard.router, prefix="/api/v1")
app.include_router(increaseBalance.router, prefix="/api/v1")


