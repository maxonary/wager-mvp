from fastapi import APIRouter, HTTPException
import requests
import urllib.parse
from app.config import load_env

router = APIRouter()

API_URL = "https://api.clashroyale.com/v1/players/{}/battlelog"
config = load_env()
API_KEY = config['API_KEY']

@router.get("/battlelog/{player_tag}")
def get_battle_log(player_tag: str):
    player_tag_encoded = urllib.parse.quote(player_tag)  # URL-encode the player_tag
    url = API_URL.format(player_tag_encoded)
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching battle log")
