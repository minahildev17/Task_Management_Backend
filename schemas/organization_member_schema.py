from pydantic import BaseModel


class OrganizationMemberCreate(BaseModel):
    UserID: int
    OrganizationID: int
    RoleID: int


class OrganizationMemberResponse(BaseModel):
    message: str