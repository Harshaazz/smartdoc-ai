from fastapi import APIRouter
from app.database.mongodb import db

router = APIRouter()

@router.get("/test-db")
async def test_db():

    collections = await db.list_collection_names()

    return {
        "status": "success",
        "collections": collections
    }