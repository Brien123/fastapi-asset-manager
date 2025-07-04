from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Asset, Transaction, TransactionType
from app.database import get_db
from app.routers.auth import get_current_user
from datetime import datetime, timedelta
from app.schemas import ReportResponse

router = APIRouter()

@router.get("/", response_model=ReportResponse)
def get_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    asset_summary = db.query(
        func.count(Asset.id),
        func.sum(Asset.value)
    ).filter(Asset.owner_id == current_user.id).one()
    
    total_assets = asset_summary[0]
    total_asset_value = asset_summary[1] or 0.0
    
    # Recent transactions (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_transactions_count = db.query(func.count(Transaction.id)).filter(
        Transaction.user_id == current_user.id,
        Transaction.timestamp >= week_ago
    ).scalar()
    
    # Transaction types distribution
    transaction_types_query_result = db.query(
        Transaction.type,
        func.count(Transaction.id)
    ).filter(
        Transaction.user_id == current_user.id
    ).group_by(Transaction.type).all()
    
    transaction_distribution = {t_type: 0 for t_type in TransactionType}
    transaction_distribution.update(dict(transaction_types_query_result))
    
    return {
        "total_assets": total_assets,
        "total_asset_value": round(total_asset_value, 2),
        "recent_transactions": recent_transactions_count,
        "transaction_types_distribution": transaction_distribution
    }