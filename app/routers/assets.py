from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AssetCreate, Asset as AssetSchema, PaginatedAssetResponse
from app.models import Asset, User
from app.database import get_db
from app.routers.auth import get_current_admin_user

router = APIRouter()

@router.post("/", response_model=AssetSchema, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset: AssetCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Check if owner exists
    owner = db.query(User).filter(User.id == asset.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail=f"User with id {asset.owner_id} not found")

    db_asset = Asset(
        name=asset.name,
        type=asset.type,
        value=asset.value,
        owner_id=asset.owner_id
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/", response_model=PaginatedAssetResponse)
def read_assets(
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(20, ge=1, le=200, description="Number of items per page"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # total count of all assets
    total_count = db.query(Asset).count()

    # assets for the current page
    skip = (page - 1) * limit
    assets = db.query(Asset).offset(skip).limit(limit).all()

    has_next_page = (skip + len(assets)) < total_count
    has_previous_page = page > 1

    return {
        "total_count": total_count,
        "page": page,
        "limit": limit,
        "has_next_page": has_next_page,
        "has_previous_page": has_previous_page,
        "assets": assets,
    }