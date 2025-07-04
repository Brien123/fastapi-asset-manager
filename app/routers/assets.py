from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AssetCreate, Asset as AssetSchema
from app.models import Asset, User
from app.database import get_db
from app.routers.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=AssetSchema)
def create_asset(
    asset: AssetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_asset = Asset(
        name=asset.name,
        type=asset.type,
        value=asset.value,
        owner_id=current_user.id
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/", response_model=List[AssetSchema])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assets = db.query(Asset).filter(Asset.owner_id == current_user.id).offset(skip).limit(limit).all()
    return assets