from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import date
from app.models import User, Asset, Transaction
from app.database import get_db
from app.routers.auth import get_current_admin_user
from typing import Dict, Any, Optional

router = APIRouter()

@router.get("/graphs")
def get_platform_graph_data(
    start_date: Optional[date] = Query(None, description="Filter data from this date. Format: YYYY-MM-DD, it is optional"),
    end_date: Optional[date] = Query(None, description="Filter data up to this date. Format: YYYY-MM-DD, it is optional"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date."
        )

    # Define reusable column expressions for casting to Date
    user_date_col = func.strftime('%Y-%m-%d', User.created_at)
    asset_date_col = func.strftime('%Y-%m-%d', Asset.created_at)
    transaction_date_col = func.strftime('%Y-%m-%d', Transaction.timestamp)

    # User growth data
    user_growth_query = db.query(
        user_date_col.label("date"),
        func.count(User.id).label("count")
    )
    if start_date:
        user_growth_query = user_growth_query.filter(user_date_col >= start_date.isoformat())
    if end_date:
        user_growth_query = user_growth_query.filter(user_date_col <= end_date.isoformat())
    user_growth = user_growth_query.group_by(user_date_col).order_by(user_date_col).all()

    # Base query for platform assets with date filters
    platform_asset_query = db.query(Asset)
    if start_date:
        platform_asset_query = platform_asset_query.filter(asset_date_col >= start_date.isoformat())
    if end_date:
        platform_asset_query = platform_asset_query.filter(asset_date_col <= end_date.isoformat())
    
    platform_total_asset_value_by_date = platform_asset_query.with_entities(
        asset_date_col.label("date"),
        func.sum(Asset.value).label("total_value")
    ).group_by(asset_date_col).order_by(asset_date_col).all()

    platform_asset_distribution = platform_asset_query.with_entities(
        Asset.type,
        func.count(Asset.id).label("count"),
        func.sum(Asset.value).label("total_value")
    ).group_by(Asset.type).all()

    # Base query for platform transactions with date filters
    platform_transaction_query = db.query(Transaction)
    if start_date:
        platform_transaction_query = platform_transaction_query.filter(transaction_date_col >= start_date.isoformat())
    if end_date:
        platform_transaction_query = platform_transaction_query.filter(transaction_date_col <= end_date.isoformat())

    platform_transaction_volume = platform_transaction_query.with_entities(
        transaction_date_col.label("date"),
        func.sum(Transaction.amount).label("volume")
    ).group_by(transaction_date_col).order_by(transaction_date_col).all()

    platform_average_transaction_size_by_date = platform_transaction_query.with_entities(
        transaction_date_col.label("date"),
        func.avg(Transaction.amount).label("avg_size")
    ).group_by(transaction_date_col).order_by(transaction_date_col).all()

    return {
        "user_growth": {
            "dates": [item.date for item in user_growth],
            "counts": [item.count for item in user_growth]
        },
        "asset_distribution": {
            "types": [item.type.value for item in platform_asset_distribution],
            "counts": [item.count for item in platform_asset_distribution],
            "values": [float(item.total_value or 0) for item in platform_asset_distribution]
        },
        "transaction_volume": {
            "dates": [item.date for item in platform_transaction_volume],
            "volumes": [float(item.volume or 0) for item in platform_transaction_volume]
        },
        "total_asset_value_by_date": {
            "dates": [item.date for item in platform_total_asset_value_by_date],
            "values": [round(float(item.total_value or 0), 2) for item in platform_total_asset_value_by_date]
        },
        "average_transaction_size_by_date": {
            "dates": [item.date for item in platform_average_transaction_size_by_date],
            "avg_sizes": [round(float(item.avg_size or 0), 2) for item in platform_average_transaction_size_by_date]
        },
    }