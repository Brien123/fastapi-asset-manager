from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, assets, transactions, reports, analytics, auth
from app.database import engine
from app.models import Base
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Codexbase Network API",
    description="Backend API for Codexbase Network hiring process",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "oauth2RedirectUrl": "/docs/oauth2-redirect",
        }
    )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Token API",
        version="1.0.0",
        description="API description",
        routes=app.routes,
    )
    
    # Basic Auth for login and Bearer for other endpoints
    openapi_schema["components"]["securitySchemes"] = {
        "BasicAuth": {
            "type": "http",
            "scheme": "basic",
            "description": "Login with username/password to get JWT token"
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token from /auth/token"
        }
    }
    
    # security requirements
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if path == "/auth/token" and method == "post":
                operation["security"] = [{"BasicAuth": []}]
            elif "auth" not in path:
                operation["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])