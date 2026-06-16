from app.database.mongodb import db
from app.utils.security import (
    hash_password,
    verify_password
)
from app.utils.jwt_handler import (
    create_access_token
)

async def register_user(user):

    existing_user = await db.users.find_one(
        {"email": user.email}
    )

    if existing_user:
        return {
            "success": False,
            "message": "Email already exists"
        }

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(
            user.password
        )
    }

    await db.users.insert_one(new_user)

    return {
        "success": True,
        "message": "User registered successfully"
    }


async def login_user(user):

    db_user = await db.users.find_one(
        {"email": user.email}
    )

    if not db_user:
        return None

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        return None

    token = create_access_token(
        {
            "email": db_user["email"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }