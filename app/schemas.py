from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models import AssetType, TransactionType, UserRole

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
    role: UserRole = UserRole.USER

class User(UserBase):
    id: int
    created_at: datetime
    role: UserRole
    
    class Config:
        orm_mode = True

class PaginatedUserResponse(BaseModel):
    total_count: int
    page: int
    limit: int
    has_next_page: bool
    has_previous_page: bool
    users: List[User]

class AssetBase(BaseModel):
    name: str
    type: AssetType
    value: float

class AssetCreate(AssetBase):
    owner_id: int

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
    average_asset_value: float
    recent_transactions: int
    transaction_types_distribution: Dict[TransactionType, int]
    asset_types_distribution: Dict[AssetType, int]
    most_valuable_asset: Optional[Asset] = None

class TransactionCreate(BaseModel):
    asset_id: int
    to_user_id: int
    type: TransactionType
    amount: Optional[float] = 0.0

class Transaction(BaseModel):
    id: int
    amount: float
    type: TransactionType
    asset_id: int
    user_id: int
    from_owner_id: int
    to_owner_id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str