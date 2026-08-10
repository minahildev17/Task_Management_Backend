from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.organization_members import OrganizationMember
from models.user import User
from models.organization import Organization
from models.role import Role

from schemas.organization_member_schema import (
    OrganizationMemberCreate,
    OrganizationMemberRemove,
    OrganizationOwnerTransfer,
    OrganizationMemberResponse
)

from utils.security import get_current_user


router = APIRouter(
    prefix="/organization-members",
    tags=["Organization Members"]
)


# --------------------------------------------------
# ASSIGN USER TO ORGANIZATION
# --------------------------------------------------

@router.post(
    "/assign",
    response_model=OrganizationMemberResponse
)
def assign_user_to_organization(
    data: OrganizationMemberCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    current_user_id = int(current_user)

    # Check organization
    organization = db.query(Organization).filter(
        Organization.OrganizationID == data.OrganizationID
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    # Check current user is Owner
    owner_role = db.query(Role).filter(
        Role.RoleName == "Owner"
    ).first()

    if not owner_role:
        raise HTTPException(
            status_code=500,
            detail="Owner role not found"
        )

    owner = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == data.OrganizationID,
        OrganizationMember.UserID == current_user_id,
        OrganizationMember.RoleID == owner_role.RoleID
    ).first()

    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Only the organization owner can assign users"
        )

    # Check user
    user = db.query(User).filter(
        User.UserID == data.UserID
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check if already a member
    existing_member = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == data.OrganizationID,
        OrganizationMember.UserID == data.UserID
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this organization"
        )

    # Check requested role
    role = db.query(Role).filter(
        Role.RoleID == data.RoleID
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    # Prevent assigning Owner role through normal assign endpoint
    if role.RoleName == "Owner":
        raise HTTPException(
            status_code=400,
            detail="Use transfer-owner endpoint to assign Owner role"
        )

    # Create membership
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


# --------------------------------------------------
# REMOVE USER FROM ORGANIZATION
# --------------------------------------------------

@router.delete(
    "/remove",
    response_model=OrganizationMemberResponse
)
def remove_user_from_organization(
    data: OrganizationMemberRemove,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    current_user_id = int(current_user)

    # Check organization
    organization = db.query(Organization).filter(
        Organization.OrganizationID == data.OrganizationID
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    # Find Owner role
    owner_role = db.query(Role).filter(
        Role.RoleName == "Owner"
    ).first()

    if not owner_role:
        raise HTTPException(
            status_code=500,
            detail="Owner role not found"
        )

    # Check current user is Owner
    owner = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == data.OrganizationID,
        OrganizationMember.UserID == current_user_id,
        OrganizationMember.RoleID == owner_role.RoleID
    ).first()

    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Only the organization owner can remove users"
        )

    # Find member
    member = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == data.OrganizationID,
        OrganizationMember.UserID == data.UserID
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="User is not a member of this organization"
        )

    # Owner cannot be removed
    if member.RoleID == owner_role.RoleID:
        raise HTTPException(
            status_code=400,
            detail="Organization owner cannot be removed"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "User removed from organization successfully"
    }


# --------------------------------------------------
# TRANSFER ORGANIZATION OWNER
# --------------------------------------------------

@router.put(
    "/transfer-owner",
    response_model=OrganizationMemberResponse
)
def transfer_organization_owner(
    data: OrganizationOwnerTransfer,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    current_user_id = int(current_user)

    # Check organization
    organization = db.query(Organization).filter(
        Organization.OrganizationID == data.OrganizationID
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    # Find Owner role
    owner_role = db.query(Role).filter(
        Role.RoleName == "Owner"
    ).first()

    if not owner_role:
        raise HTTPException(
            status_code=500,
            detail="Owner role not found"
        )

    # Find Member role
    member_role = db.query(Role).filter(
        Role.RoleName == "Member"
    ).first()

    if not member_role:
        raise HTTPException(
            status_code=500,
            detail="Member role not found"
        )

    # Check current user is Owner
    current_owner = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == data.OrganizationID,
        OrganizationMember.UserID == current_user_id,
        OrganizationMember.RoleID == owner_role.RoleID
    ).first()

    if not current_owner:
        raise HTTPException(
            status_code=403,
            detail="Only the current owner can transfer ownership"
        )

    # Owner cannot transfer to himself
    if current_user_id == data.NewOwnerID:
        raise HTTPException(
            status_code=400,
            detail="You are already the organization owner"
        )

    # New owner must already be a member
    new_owner = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == data.OrganizationID,
        OrganizationMember.UserID == data.NewOwnerID
    ).first()

    if not new_owner:
        raise HTTPException(
            status_code=404,
            detail="New owner must already be a member of the organization"
        )

    # Transfer ownership
    current_owner.RoleID = member_role.RoleID
    new_owner.RoleID = owner_role.RoleID

    db.commit()

    return {
        "message": "Organization ownership transferred successfully"
    }