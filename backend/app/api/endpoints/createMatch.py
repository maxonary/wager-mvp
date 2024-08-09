from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import match_collection, user_collection
from app.models.matchModel import Match
from datetime import datetime, timezone
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
        # Check if userTag1 and userTag2 are the same
        if request.userTag1 == request.userTag2:
            raise HTTPException(status_code=400, detail="The same userTag cannot be used for both players.")

        # Check if the bet amount is greater than 0
        if request.betAmount <= 0:
            raise HTTPException(status_code=400, detail=f"Bet amount must be greater than 0.")

        # Fetch the balance of both players
        player1 = user_collection.find_one({"userTag": request.userTag1})
        player2 = user_collection.find_one({"userTag": request.userTag2})

        # Ensure both players exist in the database
        if not player1 or not player2:
            raise HTTPException(status_code=404, detail="One or both players not found.")

        # Check if both players have sufficient balance
        if player1['balance'] < request.betAmount:
            raise HTTPException(status_code=400, detail=f"Player {request.userTag1} does not have sufficient balance.")
        if player2['balance'] < request.betAmount:
            raise HTTPException(status_code=400, detail=f"Player {request.userTag2} does not have sufficient balance.")

        # Create a MatchID
        matchID = str(uuid.uuid4())

        # Create a new match object with createdTime
        new_match = Match(
            matchID=matchID,
            userTag1=request.userTag1,
            userTag2=request.userTag2,
            betAmount=request.betAmount,
            checked=False,
            createdTime=datetime.now(timezone.utc)  # Record the created time
        )
        
        # Insert the match into the database
        result = match_collection.insert_one(new_match.dict(by_alias=True))

        print(new_match.matchID)

        # Return success response
        return {
            "message": "Success",
            "matchID": new_match.matchID,
            "betAmount": new_match.betAmount,
            "createdTime": new_match.createdTime.isoformat()  # Return createdTime as well
        }
    
    except Exception as e:
        # Handle exceptions and return a 500 error response
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the match: {str(e)}")
