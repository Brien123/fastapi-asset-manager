from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, assets, transactions, reports, analytics, auth
from app.database import engine, SessionLocal
from app.models import Base, User, UserRole
from app.routers.auth import get_password_hash

def create_default_admin_on_startup():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            hashed_password = get_password_hash("12345678")
            default_admin = User(
                username="admin",
                email="admin@test.com",
                hashed_password=hashed_password,
                role=UserRole.ADMIN
            )
            db.add(default_admin)
            db.commit()
            print("INFO:     Default admin user 'admin' created.")
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Asset Management Backend",
    description="Asset Management Backend",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    create_default_admin_on_startup()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])