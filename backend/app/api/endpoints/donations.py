from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.models.transactionModel import Transaction
from app.services.donation_service import fetch_and_process_donations 
from app.db import transaction_collection

router = APIRouter()

@router.post("/update_donations", response_model=List[Dict[str, str]])
async def update_donations():
    try:
        new_transactions = await fetch_and_process_donations()
        response_data = []
        for transaction in new_transactions:
            donor_info = {
                "username": transaction.username, 
                "GameTag": transaction.username
            }
            response_data.append(donor_info)

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions", response_model=List[Transaction])
async def fetch_all_transactions():
    try:
        # Fetch all transactions from the transaction collection
        transactions_cursor = transaction_collection.find({}, {"_id": 0})  # Exclude MongoDB's internal _id field
        transactions = list(transactions_cursor)

        # Return the transactions in the response
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")