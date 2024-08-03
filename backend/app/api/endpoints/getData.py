from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
import time
from app.services.battlelog import fetch_battle_logs, determine_winner, find_specific_opp_battle

router = APIRouter()

@router.post("/battlelog/{username}")
def get_battle_log(username: str):
    username_battlelog = fetch_battle_logs(username)
    if username_battlelog:
        return username_battlelog

@router.post("/battlelog/")
def get_dual_battle_log(username: str, opponent: str):
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(minutes=7)

    while datetime.now(timezone.utc) < end_time:
        username_battlelog = fetch_battle_logs(username)
        if username_battlelog:
            winner = determine_winner(username, opponent, username_battlelog, datetime.now(timezone.utc))
            if winner:
                return winner
        time.sleep(10)  # Sleep for 10 seconds before trying again

    raise HTTPException(status_code=404, detail="No matching battles found within the time frame")

# Get battlelog for specific opponent
@router.get("/battlelog/{username}/{opponent}")
def get_specific_opp_battle_log(username: str, opponent: str):
    username_battlelog = fetch_battle_logs(username)
    if username_battlelog:
        battle = find_specific_opp_battle(username_battlelog, opponent)
        if battle:
            return battle

    raise HTTPException(status_code=404, detail="No matching battles found with the specified opponent")