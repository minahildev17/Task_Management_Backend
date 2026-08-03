from datetime import datetime
from pydantic import BaseModel


class OrganizationBase(BaseModel):
    Name: str
    Email: str
    ContactNo: str
    Logo: str | None = None
    Theme: str | None = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    OrganizationID: int
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True