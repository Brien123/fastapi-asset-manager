from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, Transaction as TransactionSchema
from app.models import Transaction, User, Asset, TransactionType
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = db.query(Asset).filter(
        Asset.id == transaction.asset_id,
        Asset.owner_id == current_user.id
    ).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found or doesn't belong to user")
    
    if transaction.type == TransactionType.BUY:
        asset.value += transaction.amount
    elif transaction.type == TransactionType.SELL:
        if asset.value < transaction.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot sell more than the asset's current value of {asset.value}"
            )
        asset.value -= transaction.amount
    
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