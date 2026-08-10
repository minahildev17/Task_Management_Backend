from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from database import get_db

from schemas.auth_schema import (
    SignupRequest,
    LoginRequest,
    SignupResponse,
    LoginResponse
)


from services.auth_service import (
    get_user_by_email,
    create_user,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post(
    "/signup",
    response_model=SignupResponse
)
def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user_data.Email
    )


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    new_user = create_user(
        db=db,
        name=user_data.Name,
        email=user_data.Email,
        password=user_data.Password
    )


    return {
        "message": "User signup successful",
        "user_id": new_user.UserID
    }




@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    result = login_user(
        db=db,
        email=login_data.Email,
        password=login_data.Password
    )


    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    return result