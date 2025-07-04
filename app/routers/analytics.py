from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import User, Asset, Transaction
from app.database import get_db
from app.routers.auth import get_current_user
from typing import Dict, Any

router = APIRouter()

@router.get("/graphs")
def get_graph_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # User growth data
    user_growth = db.query(
        func.strftime('%Y-%m-%d', User.created_at).label("date"),
        func.count(User.id).label("count")
    ).group_by("date").order_by("date").all()
    
    # Asset distribution by type
    asset_distribution = db.query(
        Asset.type,
        func.count(Asset.id).label("count"),
        func.sum(Asset.value).label("total_value")
    ).filter(
        Asset.owner_id == current_user.id
    ).group_by(Asset.type).all()
    
    # Transaction volume over time
    transaction_volume = db.query(
        func.strftime('%Y-%m-%d', Transaction.timestamp).label("date"),
        func.sum(Transaction.amount).label("volume")
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).group_by("date").order_by("date").all()
    
    return {
        "user_growth": {
            "dates": [str(item.date) for item in user_growth],
            "counts": [item.count for item in user_growth]
        },
        "asset_distribution": {
            "types": [item.type for item in asset_distribution],
            "counts": [item.count for item in asset_distribution],
            "values": [float(item.total_value or 0) for item in asset_distribution]
        },
        "transaction_volume": {
            "dates": [str(item.date) for item in transaction_volume],
            "volumes": [float(item.volume or 0) for item in transaction_volume]
        }
    }