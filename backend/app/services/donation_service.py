import os
import httpx
from bs4 import BeautifulSoup
import json
from datetime import datetime
from app.models.transactionModel import Transaction
from typing import List
from dotenv import load_dotenv
import re
from app.db import user_collection, transaction_collection

load_dotenv()

POOL_URL = os.getenv("PAYPAL_POOL_URL")

def extract_game_tag(note: str) -> str:
    """
    Extracts the GameTag from a given note.
    A GameTag starts with # and is between 7 and 10 characters long.
    """
    match = re.search(r'#\w{6,9}', note)
    return match.group(0) if match else "No GameTag Found"

async def fetch_paypal_transactions() -> List[dict]:
    async with httpx.AsyncClient() as client:
        res = await client.get(POOL_URL)

    soup = BeautifulSoup(res.text, 'html.parser')
    store_data = soup.find(id="store").get_text()

    data = json.loads(store_data)
    transactions = data["txns"]["list"]

    processed_transactions = []
    for pt in transactions:
        # Extract GameTag from the donation note
        note = pt.get("note", "")
        game_tag = extract_game_tag(note)
        username = pt.get("name", "Unknown Donor")
        time = pt.get("date")
        amount = float(pt.get("amount", 0))

        # Ensure all required fields are included in the dictionary
        processed_transactions.append({
            'username': username,
            'GameTag': game_tag,
            'time': time,
            'amount': amount
        })

    # Sort and filter new transactions based on time
    processed_transactions.sort(key=lambda x: datetime.fromisoformat(x['time']), reverse=True)
    last_time = get_time_of_last_paypal_transaction()
    new_transactions = [t for t in processed_transactions if datetime.fromisoformat(t['time']) > last_time]

    return new_transactions

def get_time_of_last_paypal_transaction() -> datetime:
    last_transaction = user_collection.find_one(
        {}, 
        sort=[("lastProcessedBattleTime", -1)]
    )
    if not last_transaction:
        return datetime.min  # If no transactions are recorded, return earliest possible datetime
    return datetime.fromisoformat(last_transaction["lastProcessedBattleTime"])

def update_user_balance(username: str, amount: float):
    existing_user = user_collection.find_one({"userTag": username})
    if not existing_user:
        print(f"Warning: User '{username}' not found. Skipping transaction.")
        return
    
    new_balance = existing_user['balance'] + amount
    user_collection.update_one({"userTag": username}, {"$set": {"balance": new_balance}})

async def fetch_and_process_donations():
    new_transactions_dicts = await fetch_paypal_transactions()

    # Convert each dictionary to an instance of the Transaction model
    new_transactions = [
        Transaction(**transaction_dict) for transaction_dict in new_transactions_dicts
    ]

    for transaction in new_transactions:
        update_user_balance(transaction.username, transaction.amount)
        user_collection.update_one({"userTag": transaction.username}, {"$set": {"lastProcessedBattleTime": transaction.time}})

    return new_transactions