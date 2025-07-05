from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas import UserCreate, User as UserSchema, PaginatedUserResponse
from app.models import User
from app.database import get_db
from app.routers.auth import get_password_hash, get_current_user

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        if db_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=PaginatedUserResponse)
def read_users(
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(20, ge=1, le=200, description="Number of items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_count = db.query(User).count()

    skip = (page - 1) * limit
    users = db.query(User).offset(skip).limit(limit).all()

    has_next_page = (skip + len(users)) < total_count
    has_previous_page = page > 1

    return {
        "total_count": total_count,
        "page": page,
        "limit": limit,
        "has_next_page": has_next_page,
        "has_previous_page": has_previous_page,
        "users": users,
    }