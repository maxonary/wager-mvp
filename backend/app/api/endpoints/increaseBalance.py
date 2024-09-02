from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import user_collection

router = APIRouter()

# Request model for increasing balance
class IncreaseBalanceRequest(BaseModel):
    userTag: str
    increaseAmount: float

@router.post("/user/increase-balance")
async def increase_balance(request: IncreaseBalanceRequest):
    userTag = request.userTag
    increaseAmount = request.increaseAmount

    # Validate the increaseAmount
    if increaseAmount <= 0:
        raise HTTPException(status_code=400, detail="Increase amount must be greater than zero.")
    if increaseAmount >= 50:
        raise HTTPException(status_code=400, detail="Increase amount too large.")

    # Check if the user exists in the database
    existing_user = user_collection.find_one({"userTag": userTag})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Increase the user's balance
    updated_balance = existing_user['balance'] + increaseAmount
    user_collection.update_one({"userTag": userTag}, {"$set": {"balance": updated_balance}})

    return {"message": "Balance updated successfully", "userTag": userTag, "newBalance": updated_balance}