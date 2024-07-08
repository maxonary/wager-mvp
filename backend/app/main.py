from fastapi import FastAPI
from app.api.endpoints import getData

app = FastAPI()

app.include_router(getData.router, prefix="/api/v1")