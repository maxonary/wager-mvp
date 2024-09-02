import os
import httpx
from bs4 import BeautifulSoup
import json
from datetime import datetime
from app.models.transactionModel import Transaction
from typing import List
from dotenv import load_dotenv
from app.db import user_collection 

load_dotenv()

POOL_URL = os.getenv("PAYPAL_POOL_URL")

async def fetch_paypal_transactions() -> List[Transaction]:
    async with httpx.AsyncClient() as client:
        res = await client.get(POOL_URL)

    soup = BeautifulSoup(res.text, 'html.parser')
    store_data = soup.find(id="store").get_text()

    data = json.loads(store_data)
    transactions = data["txns"]["list"]

    processed_transactions = []
    for pt in transactions:
        username = pt.get("note", "error").replace(r"[^a-zA-Z0-9-]", "").lower()
        transaction = Transaction(
            username=username,
            time=pt["date"],
            amount=float(pt["amount"])
        )
        processed_transactions.append(transaction)

    processed_transactions.sort(key=lambda x: datetime.fromisoformat(x.time), reverse=True)
    last_time = get_time_of_last_paypal_transaction()
    new_transactions = [t for t in processed_transactions if datetime.fromisoformat(t.time) > last_time]

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
    new_transactions = await fetch_paypal_transactions()

    for transaction in new_transactions:
        update_user_balance(transaction.username, transaction.amount)
        user_collection.update_one({"userTag": transaction.username}, {"$set": {"lastProcessedBattleTime": transaction.time}})

    return new_transactions