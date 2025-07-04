from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models import AssetType, TransactionType

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class AssetBase(BaseModel):
    name: str
    type: AssetType
    value: float

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class PaginatedAssetResponse(BaseModel):
    total_count: int
    page: int
    limit: int
    has_next_page: bool
    has_previous_page: bool
    assets: List[Asset]

class ReportResponse(BaseModel):
    total_assets: int
    total_asset_value: float
    recent_transactions: int
    transaction_types_distribution: Dict[TransactionType, int]

class TransactionBase(BaseModel):
    amount: float
    type: TransactionType
    asset_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str