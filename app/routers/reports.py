from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Asset, Transaction, TransactionType, AssetType
from app.database import get_db
from app.routers.auth import get_current_admin_user
from datetime import datetime, timedelta
from app.schemas import ReportResponse

router = APIRouter()

@router.get("/", response_model=ReportResponse)
def get_platform_report(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):

    asset_summary = db.query(
        func.count(Asset.id),
        func.sum(Asset.value)
    ).one()
    
    total_assets = asset_summary[0]
    total_asset_value = asset_summary[1] or 0.0
    average_asset_value = total_asset_value / total_assets if total_assets > 0 else 0.0
    
    # Recent transactions (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_transactions_count = db.query(func.count(Transaction.id)).filter(
        Transaction.timestamp >= week_ago
    ).scalar()
    
    # Transaction types distribution
    transaction_types_query_result = db.query(
        Transaction.type,
        func.count(Transaction.id)
    ).group_by(Transaction.type).all()
    
    transaction_distribution = {t_type: 0 for t_type in TransactionType}
    transaction_distribution.update(dict(transaction_types_query_result))
    
    # Asset types distribution
    asset_types_query_result = db.query(
        Asset.type,
        func.count(Asset.id)
    ).group_by(Asset.type).all()
    
    asset_distribution = {a_type: 0 for a_type in AssetType}
    asset_distribution.update(dict(asset_types_query_result))

    # Most valuable asset
    most_valuable_asset = db.query(Asset).order_by(Asset.value.desc()).first()

    return {
        "total_assets": total_assets,
        "total_asset_value": round(total_asset_value, 2),
        "average_asset_value": round(average_asset_value, 2),
        "recent_transactions": recent_transactions_count,
        "transaction_types_distribution": transaction_distribution,
        "asset_types_distribution": asset_distribution,
        "most_valuable_asset": most_valuable_asset
    }