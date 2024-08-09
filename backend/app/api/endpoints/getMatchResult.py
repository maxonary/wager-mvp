from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import match_collection, user_collection, get_db_client
from app.services.battlelog import determine_winner
from datetime import datetime, timezone

router = APIRouter()

# Define a Pydantic model for the request body
class MatchResultRequest(BaseModel):
    matchID: str

@router.post("/match/result")
async def get_match_result(request: MatchResultRequest):
    db_client = get_db_client()
    session = db_client.start_session()
    session.start_transaction()

    try:
        matchID = request.matchID

        # Step 1: Fetch the match details from the database
        match = match_collection.find_one({"matchID": matchID}, session=session)
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")

        # Step 2: Check if the match has already been checked
        if match.get("checked"):
            raise HTTPException(status_code=400, detail="This match result has already been processed.")

        userTag1 = match['userTag1']
        userTag2 = match['userTag2']
        betAmount = match['betAmount']

        # Step 3: Determine the winner using the Clash Royale API
        winner = determine_winner(userTag1, userTag2, datetime.now(timezone.utc))
        if winner is None:
            # Update the match to indicate it was a draw and set checkedTime
            match_collection.update_one(
                {"matchID": matchID},
                {"$set": {
                    "checked": True,
                    "checkedTime": datetime.now(timezone.utc)
                }},
                session=session
            )
            session.commit_transaction()
            return {
                "message": "It's a draw",
                "matchID": matchID,
                "betAmount": betAmount
            }

        # Step 4: Update the match record in the database
        winnerTag = winner['winner']
        checked_time = datetime.now(timezone.utc)
        match_collection.update_one(
            {"matchID": matchID},
            {"$set": {
                "winnerUserID": winnerTag,
                "checked": True,
                "checkedTime": checked_time
            }},
            session=session
        )

        # Step 5: Update the user balances and wins atomically
        loserTag = userTag1 if winnerTag == userTag2 else userTag2
        latest_battle_time_str = checked_time.strftime("%Y%m%dT%H%M%S.%fZ")

        # Update winner balance and wins
        user_collection.update_one(
            {"userTag": winnerTag},
            {
                "$inc": {"balance": betAmount, "wins": 1},
                "$set": {"lastProcessedBattleTime": latest_battle_time_str}
            },
            session=session
        )

        # Update loser balance and lastProcessedBattleTime
        user_collection.update_one(
            {"userTag": loserTag},
            {
                "$inc": {"balance": -betAmount},
                "$set": {"lastProcessedBattleTime": latest_battle_time_str}
            },
            session=session
        )

        # Retrieve the updated balances of both players
        updated_winner = user_collection.find_one({"userTag": winnerTag}, session=session)
        updated_loser = user_collection.find_one({"userTag": loserTag}, session=session)

        # Commit the transaction
        session.commit_transaction()

        # Return the match result, including the updated balances
        return {
            "message": "Success",
            "matchID": matchID,
            "winnerUserTag": winnerTag,
            "loserUserTag": loserTag,
            "betAmount": betAmount,
            "winnerUserName": updated_winner['username'],
            "loserUserName": updated_loser['username'],
            "checkedTime": checked_time.isoformat(),
            "winnerNewBalance": updated_winner['balance'],
            "loserNewBalance": updated_loser['balance']
        }

    except HTTPException as e:
        session.abort_transaction()
        raise e
    except Exception as e:
        session.abort_transaction()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the match result: {str(e)}")
    finally:
        session.end_session()
