from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ThemeEnum(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"


class OrganizationBase(BaseModel):
    Name: str
    Email: str
    ContactNo: str
    Theme: ThemeEnum = ThemeEnum.LIGHT


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(BaseModel):
    OrganizationID: int
    Name: str
    Email: str
    ContactNo: str
    LogoURL: str | None = None
    Theme: ThemeEnum
    CreatedAt: datetime
    UpdatedAt: datetime

    model_config = ConfigDict(
        from_attributes=True
    )