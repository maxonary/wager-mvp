import requests
import urllib.parse
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.config import load_env 

config = load_env()
API_KEY = config['API_KEY']
API_URL = "https://api.clashroyale.com/v1/players/{}/battlelog"

def fetch_battle_logs(username: str):
    username_encoded = urllib.parse.quote(username)
    username_url = API_URL.format(username_encoded)

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    username_response = requests.get(username_url, headers=headers)

    if username_response.status_code != 200:
        print(f"Error: {username_response.text}")
        raise HTTPException(status_code=username_response.status_code, detail="Error fetching username battle log")

    return username_response.json()

def determine_winner(username, opponent, username_battlelog, current_time):
    min_time_diff = timedelta(minutes=14)
    closest_match = None

    for battle in username_battlelog:
        battle_time = datetime.strptime(battle['battleTime'], "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)
        if current_time - timedelta(minutes=14) <= battle_time <= current_time:
            if not closest_match or abs(battle_time - current_time) < abs(closest_match['battleTime'] - current_time):
                if any(player['tag'] == opponent for player in battle['opponent']):
                    closest_match = battle

    if not closest_match:
        return None

    username_crowns = sum(player['crowns'] for player in closest_match['team'] if player['tag'] == username)
    opponent_crowns = sum(player['crowns'] for player in closest_match['opponent'] if player['tag'] == opponent)

    if username_crowns > opponent_crowns:
        return {"winner": username}
    elif opponent_crowns > username_crowns:
        return {"winner": opponent}
   
