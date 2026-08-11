from fastapi import APIRouter, Depends

from utils.security import (
    get_current_user,
    require_system_admin
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# --------------------------------------------------
# GET CURRENT USER
# --------------------------------------------------

@router.get("/me")
def get_current_user_profile(
    user_id: str = Depends(get_current_user)
):

    return {
        "message": "Authenticated user",
        "user_id": user_id
    }


# --------------------------------------------------
# SYSTEM ADMIN ONLY
# --------------------------------------------------

@router.get("/system-admin")
def system_admin_test(
    admin_role_id: int = Depends(require_system_admin)
):

    return {
        "message": "System Admin access granted",
        "role_id": admin_role_id
    }
