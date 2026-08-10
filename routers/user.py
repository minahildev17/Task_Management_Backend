from fastapi import APIRouter, Depends

from utils.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_current_user_profile(
    user_id: str = Depends(get_current_user)
):

    return {
        "message": "Authenticated user",
        "user_id": user_id
    }