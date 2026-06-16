from fastapi import (
    APIRouter,
    HTTPException
)

from app.models.user_model import (
    UserRegister,
    UserLogin
)

from app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register(
    user: UserRegister
):

    result = await register_user(user)

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@router.post("/login")
async def login(
    user: UserLogin
):

    result = await login_user(user)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return result