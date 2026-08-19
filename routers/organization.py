import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from database import get_db

from models.organization import Organization
from models.organization_members import OrganizationMember
from models.role import Role
from models.theme import Theme

from schemas.organization_schema import OrganizationResponse

from utils.security import get_current_user


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


# --------------------------------------------------
# GET ALL ORGANIZATIONS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[OrganizationResponse]
)
def get_organizations(
    db: Session = Depends(get_db)
):

    return db.query(Organization).all()


# --------------------------------------------------
# GET SINGLE ORGANIZATION
# --------------------------------------------------

@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse
)
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


# --------------------------------------------------
# CREATE ORGANIZATION
# Creator automatically becomes OWNER
# --------------------------------------------------

@router.post(
    "/",
    response_model=OrganizationResponse
)
def create_organization(
    Name: str = Form(...),
    Email: str = Form(...),
    ContactNo: str = Form(...),
    ThemeID: int = Form(...),
    Logo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    # --------------------------------------------------
    # CHECK ORGANIZATION EMAIL
    # --------------------------------------------------

    existing = db.query(Organization).filter(
        Organization.Email == Email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Organization email already exists"
        )

    # --------------------------------------------------
    # CHECK THEME
    # --------------------------------------------------

    theme = db.query(Theme).filter(
        Theme.ThemeID == ThemeID
    ).first()

    if not theme:
        raise HTTPException(
            status_code=404,
            detail="Theme not found"
        )

    # --------------------------------------------------
    # CHECK OWNER ROLE
    # --------------------------------------------------

    owner_role = db.query(Role).filter(
        Role.RoleName == "Owner"
    ).first()

    if not owner_role:
        raise HTTPException(
            status_code=500,
            detail="Owner role not found"
        )

    # --------------------------------------------------
    # SAVE LOGO
    # --------------------------------------------------

    logo_path = None

    if Logo:

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        extension = ""

        if Logo.filename and "." in Logo.filename:
            extension = Logo.filename.split(".")[-1]

        if extension:
            filename = f"{uuid.uuid4()}.{extension}"
        else:
            filename = str(uuid.uuid4())

        logo_path = os.path.join(
            "uploads",
            filename
        )

        with open(
            logo_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                Logo.file,
                buffer
            )

    # --------------------------------------------------
    # CREATE ORGANIZATION
    # --------------------------------------------------

    organization = Organization(
        Name=Name,
        Email=Email,
        ContactNo=ContactNo,
        LogoURL=logo_path,
        ThemeID=ThemeID
    )

    db.add(organization)

    # Get OrganizationID
    db.flush()

    # --------------------------------------------------
    # CREATOR BECOMES OWNER
    # --------------------------------------------------

    organization_member = OrganizationMember(
        OrganizationID=organization.OrganizationID,
        UserID=user_id,
        RoleID=owner_role.RoleID
    )

    db.add(organization_member)

    db.commit()
    db.refresh(organization)

    return organization


# --------------------------------------------------
# UPDATE ORGANIZATION
# ONLY OWNER CAN UPDATE
# --------------------------------------------------

@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse
)
def update_organization(
    organization_id: int,
    Name: str = Form(...),
    Email: str = Form(...),
    ContactNo: str = Form(...),
    ThemeID: int = Form(...),
    Logo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    # --------------------------------------------------
    # CHECK ORGANIZATION
    # --------------------------------------------------

    organization = db.query(Organization).filter(
        Organization.OrganizationID == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    # --------------------------------------------------
    # CHECK OWNER ROLE
    # --------------------------------------------------

    owner_role = db.query(Role).filter(
        Role.RoleName == "Owner"
    ).first()

    if not owner_role:
        raise HTTPException(
            status_code=500,
            detail="Owner role not found"
        )

    # --------------------------------------------------
    # CHECK CURRENT USER IS OWNER
    # --------------------------------------------------

    membership = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == organization_id,
        OrganizationMember.UserID == user_id,
        OrganizationMember.RoleID == owner_role.RoleID
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Only the organization owner can update the organization"
        )

    # --------------------------------------------------
    # CHECK THEME
    # --------------------------------------------------

    theme = db.query(Theme).filter(
        Theme.ThemeID == ThemeID
    ).first()

    if not theme:
        raise HTTPException(
            status_code=404,
            detail="Theme not found"
        )

    # --------------------------------------------------
    # CHECK EMAIL
    # --------------------------------------------------

    existing_email = db.query(Organization).filter(
        Organization.Email == Email,
        Organization.OrganizationID != organization_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Organization email already exists"
        )

    # --------------------------------------------------
    # UPDATE ORGANIZATION
    # --------------------------------------------------

    organization.Name = Name
    organization.Email = Email
    organization.ContactNo = ContactNo
    organization.ThemeID = ThemeID

    # --------------------------------------------------
    # UPDATE LOGO
    # --------------------------------------------------

    if Logo:

        if (
            organization.LogoURL
            and os.path.exists(organization.LogoURL)
        ):
            os.remove(
                organization.LogoURL
            )

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        extension = ""

        if Logo.filename and "." in Logo.filename:
            extension = Logo.filename.split(".")[-1]

        if extension:
            filename = f"{uuid.uuid4()}.{extension}"
        else:
            filename = str(uuid.uuid4())

        logo_path = os.path.join(
            "uploads",
            filename
        )

        with open(
            logo_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                Logo.file,
                buffer
            )

        organization.LogoURL = logo_path

    db.commit()
    db.refresh(organization)

    return organization


# --------------------------------------------------
# DELETE ORGANIZATION
# ONLY OWNER CAN DELETE
# --------------------------------------------------

@router.delete(
    "/{organization_id}"
)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    # --------------------------------------------------
    # CHECK ORGANIZATION
    # --------------------------------------------------

    organization = db.query(Organization).filter(
        Organization.OrganizationID == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    # --------------------------------------------------
    # CHECK OWNER ROLE
    # --------------------------------------------------

    owner_role = db.query(Role).filter(
        Role.RoleName == "Owner"
    ).first()

    if not owner_role:
        raise HTTPException(
            status_code=500,
            detail="Owner role not found"
        )

    # --------------------------------------------------
    # CHECK CURRENT USER IS OWNER
    # --------------------------------------------------

    membership = db.query(OrganizationMember).filter(
        OrganizationMember.OrganizationID == organization_id,
        OrganizationMember.UserID == user_id,
        OrganizationMember.RoleID == owner_role.RoleID
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Only the organization owner can delete the organization"
        )

    # --------------------------------------------------
    # DELETE LOGO
    # --------------------------------------------------

    if (
        organization.LogoURL
        and os.path.exists(organization.LogoURL)
    ):
        os.remove(
            organization.LogoURL
        )

    # --------------------------------------------------
    # DELETE ORGANIZATION
    # --------------------------------------------------

    db.delete(organization)
    db.commit()

    return {
        "message": "Organization deleted successfully"
    }