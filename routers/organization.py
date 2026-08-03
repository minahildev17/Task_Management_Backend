from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.organization import Organization
from schemas.organization_schema import (
    OrganizationCreate,
    OrganizationResponse
)


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


# Get all organizations
@router.get("/", response_model=list[OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):

    organizations = db.query(Organization).all()

    return organizations


# Get organization by ID
@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):

    organization = db.query(Organization).filter(
        Organization.OrganizationID == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    return organization


# Create organization
@router.post("/", response_model=OrganizationResponse)
def create_organization(
    organization_data: OrganizationCreate,
    db: Session = Depends(get_db)
):

    existing_organization = db.query(Organization).filter(
        Organization.Email == organization_data.Email
    ).first()

    if existing_organization:
        raise HTTPException(
            status_code=400,
            detail="Organization email already registered"
        )

    new_organization = Organization(
        Name=organization_data.Name,
        Email=organization_data.Email,
        ContactNo=organization_data.ContactNo,
        Logo=organization_data.Logo,
        Theme=organization_data.Theme
    )

    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    return new_organization


# Update organization
@router.put("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    organization_id: int,
    organization_data: OrganizationCreate,
    db: Session = Depends(get_db)
):

    organization = db.query(Organization).filter(
        Organization.OrganizationID == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    organization.Name = organization_data.Name
    organization.Email = organization_data.Email
    organization.ContactNo = organization_data.ContactNo
    organization.Logo = organization_data.Logo
    organization.Theme = organization_data.Theme

    db.commit()
    db.refresh(organization)

    return organization


# Delete organization
@router.delete("/{organization_id}")
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):

    organization = db.query(Organization).filter(
        Organization.OrganizationID == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    db.delete(organization)
    db.commit()

    return {
        "message": "Organization deleted successfully"
    }
