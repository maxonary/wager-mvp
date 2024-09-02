from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.db import user_collection
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

class UserInfo(BaseModel):
    username: str
    userTag: str
    balance: float

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = user_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

@router.get("/user/info", response_model=UserInfo)
async def get_user_info(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user.get("username", ""),
        "userTag": user.get("userTag", ""),
        "balance": user.get("balance", 0)
    }