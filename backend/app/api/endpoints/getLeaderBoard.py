from fastapi import APIRouter, HTTPException
from app.db import user_collection

router = APIRouter()

@router.get("/leaderboard")
async def get_leaderboard():
    try:
        # Fetch all users from the collection, sorted by balance in descending order
        leaderboard = list(user_collection.find({}, {"_id": 0, "userTag": 1, "balance": 1, "wins": 1, "username": 1}).sort("balance", -1))

        # Return the leaderboard as a JSON response
        return {
            "message": "Leaderboard fetched successfully",
            "leaderboard": leaderboard
        }
    
    except Exception as e:
        # Handle exceptions and return a 500 error response
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the leaderboard: {str(e)}")
