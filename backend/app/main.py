from fastapi import FastAPI

from .api.users import router as user_router
from .api.requests import router as request_router
from .api.approvals import router as approval_router
from .api.catalog import router as catalog_router
from .api.ai_requests import router as ai_router


app = FastAPI(
    title="AI Data Access Provisioning Platform",
    description="Automated Data Access Governance System",
    version="1.0.0"
)


# Register API routes
app.include_router(user_router)
app.include_router(request_router)
app.include_router(approval_router)
app.include_router(catalog_router)
app.include_router(ai_router)


# Health Check API
@app.get("/")
def health_check():
    return {
        "message": "AI Data Access Platform is running successfully"
    }