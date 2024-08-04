from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import match_collection
from app.models.matchModel import Match
import uuid

router = APIRouter()

# Request body model
class CreateMatchRequest(BaseModel):
    userTag1: str
    userTag2: str
    betAmount: int

@router.post("/match")
async def create_match(request: CreateMatchRequest):
    try:
        # Create a MatchID
        matchID = str(uuid.uuid4())

        if request.userTag1 == request.userTag2:
            raise HTTPException(status_code=400, detail="The same userTag cannot be used for both players.")

        # Create a new match object
        new_match = Match(
            matchID=matchID,
            userTag1=request.userTag1,
            userTag2=request.userTag2,
            betAmount=request.betAmount,
            checked=False
        )
        
        # Insert the match into the database
        result = match_collection.insert_one(new_match.dict(by_alias=True))

        print(new_match.matchID)

        # Return success response
        return {
            "message": "Success",
            "matchID": new_match.matchID,
            "betAmount": new_match.betAmount
        }
    
    except Exception as e:
        # Handle exceptions and return a 500 error response
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the match: {str(e)}")
