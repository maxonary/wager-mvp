from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import user_collection
from app.models.userModel import User
from app.services.battlelog import fetch_battle_logs

router = APIRouter()

# Define the request model
class CreateUserRequest(BaseModel):
    userTag: str

@router.post("/user")
async def create_user(request: CreateUserRequest):
    userTag = request.userTag  # Extract userTag from the request body

    # Validate the userTag format
    if len(userTag) < 4:
        raise HTTPException(status_code=400, detail="Invalid user tag format")

    # Check if the user already exists in the database
    existing_user = user_collection.find_one({"userTag": userTag})
    if existing_user:
        return {"message": "User exists", "userID": str(existing_user['_id']), "balance": existing_user['balance']}
    

    ## TODO: Uncomment the following code after testing the fetch_battle_logs function

    # # Fetch battle log to validate the user exists in Clash Royale
    # try:
    #     user_battle_log = fetch_battle_logs(userTag)
    #     print(user_battle_log)
    # except HTTPException as e:
    #     raise HTTPException(status_code=404, detail="User not found in Clash Royale")

    # If user exists, create a new user in the database
    new_user = User(userTag=userTag)
    result = user_collection.insert_one(new_user.dict())

    return {"message": "Success", "userID": str(result.inserted_id), "balance": new_user.balance}
