from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    OrganizationID: int
    Name: str
    Description: str | None = None
    Status: str = "Active"
    StartDate: date | None = None
    EndDate: date | None = None


class ProjectUpdate(BaseModel):
    Name: str | None = None
    Description: str | None = None
    Status: str | None = None
    StartDate: date | None = None
    EndDate: date | None = None


class ProjectResponse(BaseModel):
    ProjectID: int
    OrganizationID: int
    CreatedBy: int
    Name: str
    Description: str | None
    Status: str
    StartDate: date | None
    EndDate: date | None
    CreatedAt: datetime
    UpdatedAt: datetime

    model_config = ConfigDict(
        from_attributes=True
    )