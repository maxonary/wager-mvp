from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.db import user_collection
from app.models.userModel import User, CreateUserRequest
from app.services.battlelog import fetch_battle_logs
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup")
async def signup(request: CreateUserRequest):
    # Check if user already exists
    existing_user = user_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate the userTag format
    if len(request.userTag) < 4:
        raise HTTPException(status_code=400, detail="Invalid user tag format")

    # Fetch battle log to validate the user exists in Clash Royale
    try:
        user_battle_log = fetch_battle_logs(request.userTag)
    except HTTPException:
        raise HTTPException(status_code=404, detail="User not found in Clash Royale")

    # Extract userName from the battle log's team section
    userName = None
    for battle in user_battle_log:
        for player in battle.get('team', []):
            if player.get('tag') == request.userTag:
                userName = player.get('name')
                break
        if userName:
            break

    # If userName is not found, set it to "Unknown"
    if not userName:
        userName = "Unknown"

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Create new user
    new_user = User(
        userTag=request.userTag,
        email=request.email,
        password=hashed_password,
        username=userName
    )
    result = user_collection.insert_one(new_user.dict())

    # Generate access token
    access_token = create_access_token(data={"sub": request.email})

    return {
        "message": "User created successfully",
        "userID": str(result.inserted_id),
        "access_token": access_token,
        "token_type": "bearer"
    }

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
async def signin(request: SignInRequest):
    user = user_collection.find_one({"email": request.email})
    if not user or not verify_password(request.password, user['password']):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user['email']})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userID": str(user['_id']),
        "userTag": user['userTag']
    }

# @router.get("/users/me")
# async def read_users_me(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except jwt.PyJWTError:
#         raise credentials_exception
#     user = user_collection.find_one({"email": email})
#     if user is None:
#         raise credentials_exception
#     return {
#         "email": user['email'],
#         "userTag": user['userTag'],
#         "username": user['username'],
#         "balance": user['balance']
#     }