from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrganizationBase(BaseModel):
    Name: str
    Email: str
    ContactNo: str
    ThemeID: int


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(BaseModel):
    OrganizationID: int
    Name: str
    Email: str
    ContactNo: str
    LogoURL: str | None = None
    ThemeID: int
    CreatedAt: datetime
    UpdatedAt: datetime

    model_config = ConfigDict(
        from_attributes=True
    )