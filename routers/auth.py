from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.auth_schema import (
    SignupRequest,
    LoginRequest,
    AuthResponse
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Signup
@router.post("/signup", response_model=AuthResponse)
def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.Email == user_data.Email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        Name=user_data.Name,
        Email=user_data.Email,
        Password=user_data.Password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User signup successful",
        "user_id": new_user.UserID
    }


# Login
@router.post("/login", response_model=AuthResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.Email == login_data.Email,
        User.Password == login_data.Password
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user_id": user.UserID
    }