import requests
import urllib.parse
from datetime import datetime, timezone
from fastapi import HTTPException
from app.db import user_collection
from app.config import load_env
import json

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

def calculate_crowns(players: list, username: str) -> int:
    return sum(player['crowns'] for player in players if 'tag' in player and player['tag'] == username)

def find_latest_battle(battlelog: list) -> dict:
    latest_battle = None

    for battle in battlelog:
        battle_time = datetime.strptime(battle['battleTime'], "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)
        if not latest_battle or battle_time > datetime.strptime(latest_battle['battleTime'], "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc):
            latest_battle = battle

    return latest_battle

def determine_winner(userTag1: str, userTag2: str, current_time: datetime) -> dict:
    userTag1_battlelog = fetch_battle_logs(userTag1)

    # Save the battle log to a JSON file for debugging
    with open(f'battlelog_{userTag1}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json', 'w') as f:
        json.dump(userTag1_battlelog, f, indent=4)

    if 'items' in userTag1_battlelog:
        latest_battle = find_latest_battle(userTag1_battlelog['items'])
        if not latest_battle:
            return None

        # Check if this battle has already been processed
        match_in_db = user_collection.find_one({"userTag": userTag1})
        last_processed_time = match_in_db.get('lastProcessedBattleTime') if match_in_db else None
        latest_battle_time = datetime.strptime(latest_battle['battleTime'], "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)

        if last_processed_time and latest_battle_time <= datetime.strptime(last_processed_time, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc):
            raise HTTPException(status_code=400, detail="This match has already been processed")

        # Ensure correct identification of team and opponent
        team_crowns = calculate_crowns(latest_battle.get('team', []), userTag1)
        opponent_crowns = calculate_crowns(latest_battle.get('opponent', []), userTag2)

        return {"winner": userTag1 if team_crowns > opponent_crowns else userTag2 if opponent_crowns > team_crowns else None}

    return None
