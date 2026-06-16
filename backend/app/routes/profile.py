from fastapi import APIRouter, Depends
from app.utils.auth_middleware import verify_token

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/")
def get_profile(
    user=Depends(verify_token)
):
    return {
        "message": "Welcome",
        "user": user
    }