from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, Transaction as TransactionSchema
from app.models import Transaction, User, Asset
from app.database import get_db
from app.routers.auth import get_current_user
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=TransactionSchema)
def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if asset belongs to user
    asset = db.query(Asset).filter(
        Asset.id == transaction.asset_id,
        Asset.owner_id == current_user.id
    ).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found or doesn't belong to user")
    
    db_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        user_id=current_user.id,
        asset_id=transaction.asset_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction