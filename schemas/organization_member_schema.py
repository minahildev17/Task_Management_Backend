from pydantic import BaseModel


class OrganizationMemberCreate(BaseModel):
    UserID: int
    OrganizationID: int
    RoleID: int


class OrganizationMemberRemove(BaseModel):
    UserID: int
    OrganizationID: int


class OrganizationOwnerTransfer(BaseModel):
    OrganizationID: int
    NewOwnerID: int


class OrganizationMemberResponse(BaseModel):
    message: str