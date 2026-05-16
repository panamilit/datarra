from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field

from app.core.security import get_current_user
from app.repositories.user_repository import (
    get_user_by_email, 
    create_user,
    update_user_display_name,
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    display_name: str = Field(min_length=2, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    display_name: str = Field(min_length=2, max_length=100)


@router.post("/register")
def register_user(payload: RegisterRequest):
    existing_user = get_user_by_email(payload.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(payload.password)

    user = create_user(
        email=payload.email,
        password_hash=password_hash,
        display_name=payload.display_name,
    )

    return user


@router.post("/login")
def login_user(payload: LoginRequest):
    user = get_user_by_email(payload.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "email": user["email"],
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "display_name": current_user["display_name"],
        "is_admin": current_user["is_admin"],
    }


@router.patch("/me")
def update_me(
    payload: UpdateProfileRequest,
    current_user=Depends(get_current_user),
):
    updated_user = update_user_display_name(
        user_id=current_user["id"],
        display_name=payload.display_name,
    )

    return updated_user