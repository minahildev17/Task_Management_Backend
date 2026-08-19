from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.project import Project
from models.organization import Organization
from schemas.project_schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)
from utils.security import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# --------------------------------------------------
# CREATE PROJECT
# --------------------------------------------------

@router.post(
    "/",
    response_model=ProjectResponse
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    organization = db.query(Organization).filter(
        Organization.OrganizationID == project_data.OrganizationID
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    project = Project(
        OrganizationID=project_data.OrganizationID,
        CreatedBy=user_id,
        Name=project_data.Name,
        Description=project_data.Description,
        Status=project_data.Status,
        StartDate=project_data.StartDate,
        EndDate=project_data.EndDate
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# --------------------------------------------------
# UPDATE PROJECT
# --------------------------------------------------

@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    project = db.query(Project).filter(
        Project.ProjectID == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    update_data = project_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


# --------------------------------------------------
# DELETE PROJECT
# --------------------------------------------------

@router.delete(
    "/{project_id}"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    project = db.query(Project).filter(
        Project.ProjectID == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }