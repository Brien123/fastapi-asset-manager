from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, Transaction as TransactionSchema
from app.models import Transaction, User, Asset, TransactionType
from app.database import get_db
from app.routers.auth import get_current_admin_user

router = APIRouter()

@router.post("/", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # check if asset exists
    asset = db.query(Asset).filter(Asset.id == transaction.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    from_owner_id = asset.owner_id
    to_owner = db.query(User).filter(User.id == transaction.to_user_id).first()

    if not to_owner:
        raise HTTPException(status_code=404, detail=f"Receiving user with id {transaction.to_user_id} not found")

    if from_owner_id == transaction.to_user_id:
        raise HTTPException(status_code=400, detail="Cannot transfer an asset to its current owner")

    transaction_amount = 0.0
    if transaction.type == TransactionType.SELL:
        if not transaction.amount or transaction.amount <= 0:
            raise HTTPException(status_code=400, detail="A positive 'amount' is required for a 'sell' transaction.")
        transaction_amount = transaction.amount
        asset.value = transaction.amount
        asset.owner_id = transaction.to_user_id
        
    elif transaction.type == TransactionType.TRANSFER:
        transaction_amount = asset.value
        asset.owner_id = transaction.to_user_id
    else:
        raise HTTPException(status_code=400, detail=f"Transaction type '{transaction.type.value}' is not supported. Use 'sell' or 'transfer'.")

    # Create transaction record
    db_transaction = Transaction(
        amount=transaction_amount,
        type=transaction.type,
        user_id=current_user.id,
        asset_id=transaction.asset_id,
        from_owner_id=from_owner_id,
        to_owner_id=transaction.to_user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction