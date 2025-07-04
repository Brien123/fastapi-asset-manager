from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Asset, Transaction
from app.database import get_db
from app.routers.auth import get_current_user
from datetime import datetime, timedelta
from typing import Dict, Any

router = APIRouter()

@router.get("/")
def get_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Total assets
    total_assets = db.query(func.count(Asset.id)).filter(
        Asset.owner_id == current_user.id
    ).scalar()
    
    # Total asset value
    total_value = db.query(func.sum(Asset.value)).filter(
        Asset.owner_id == current_user.id
    ).scalar() or 0
    
    # Recent transactions
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_transactions = db.query(func.count(Transaction.id)).filter(
        Transaction.user_id == current_user.id,
        Transaction.timestamp >= week_ago
    ).scalar()
    
    # Transaction types distribution
    transaction_types = db.query(
        Transaction.type,
        func.count(Transaction.id)
    ).filter(
        Transaction.user_id == current_user.id
    ).group_by(Transaction.type).all()
    
    return {
        "total_assets": total_assets,
        "total_asset_value": round(total_value, 2),
        "recent_transactions": recent_transactions,
        "transaction_types_distribution": dict(transaction_types)
    }