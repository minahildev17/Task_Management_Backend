from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.organization_members import OrganizationMember
from models.user import User
from models.organization import Organization
from schemas.organization_member_schema import (
    OrganizationMemberCreate,
    OrganizationMemberResponse
)


router = APIRouter(
    prefix="/organization-members",
    tags=["Organization Members"]
)


@router.post(
    "/assign",
    response_model=OrganizationMemberResponse
)
def assign_user_to_organization(
    data: OrganizationMemberCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.UserID == data.UserID
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    organization = db.query(Organization).filter(
        Organization.OrganizationID == data.OrganizationID
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )


    new_member = OrganizationMember(
        OrganizationID=data.OrganizationID,
        UserID=data.UserID,
        RoleID=data.RoleID
    )


    db.add(new_member)
    db.commit()
    db.refresh(new_member)


    return {
        "message": "User assigned to organization successfully"
    }