from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

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
    type: str
    value: float

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float
    type: str
    asset_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
class UserLogin(BaseModel):
    username: str
    password: str