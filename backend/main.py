from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.test_db import router as test_router
from app.routes.profile import router as profile_router
from app.routes.documents import router as document_router

app = FastAPI(
    title="SmartDoc AI",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(profile_router)
app.include_router(document_router)

@app.get("/")
def home():
    return {
        "message": "SmartDoc AI API Running"
    }