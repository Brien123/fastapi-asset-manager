from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class AssetType(str, enum.Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    REAL_ESTATE = "real_estate"

class TransactionType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    TRANSFER = "transfer"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="user")
    assets = relationship("Asset", back_populates="owner")

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(SQLAlchemyEnum(AssetType, name="asset_type_enum"), nullable=False)
    value = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="assets")
    transactions = relationship("Transaction", back_populates="asset")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(SQLAlchemyEnum(TransactionType, name="transaction_type_enum"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")