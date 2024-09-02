# File: api/endpoints/donations.py

from fastapi import APIRouter, HTTPException
from app.services.donation_service import fetch_and_process_donations

router = APIRouter()

@router.post("/update_donations", response_model=dict)
async def update_donations():
    try:
        new_transactions = await fetch_and_process_donations()
        return {"status": "success", "new_transactions": len(new_transactions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))