import requests
import urllib.parse
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.config import load_env 

config = load_env()
API_KEY = config['API_KEY']
API_URL = "https://api.clashroyale.com/v1/players/{}/battlelog"

def fetch_battle_logs(username: str) -> dict:
    username_encoded = urllib.parse.quote(username)
    username_url = API_URL.format(username_encoded)

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.get(username_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Error fetching username battle log")

    return response.json()

def find_closest_battle(battlelog: dict, opponent: str, current_time: datetime) -> dict:
    min_time_diff = timedelta(minutes=14)
    closest_match = None

    for battle in battlelog['items']:
        battle_time = datetime.strptime(battle['battleTime'], "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)
        if current_time - timedelta(minutes=14) <= battle_time <= current_time:
            if not closest_match or abs(battle_time - current_time) < abs(closest_match['battleTime'] - current_time):
                if any(player['tag'] == opponent for player in battle['opponent']):
                    closest_match = battle

    return closest_match

def calculate_crowns(players: list, username: str) -> int:
    return sum(player['crowns'] for player in players if player['tag'] == username)

def determine_winner(username: str, opponent: str, current_time: datetime) -> dict:
    username_battlelog = fetch_battle_logs(username)
    closest_match = find_closest_battle(username_battlelog, opponent, current_time)

    if not closest_match:
        return None

    username_crowns = calculate_crowns(closest_match['team'], username)
    opponent_crowns = calculate_crowns(closest_match['opponent'], opponent)

    if username_crowns > opponent_crowns:
        return {"winner": username}
    elif opponent_crowns > username_crowns:
        return {"winner": opponent}