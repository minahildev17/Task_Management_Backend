from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    OrganizationMemberID = Column(Integer, primary_key=True, index=True)

    OrganizationID = Column(
        Integer,
        ForeignKey("organizations.OrganizationID"),
        nullable=False
    )

    UserID = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    RoleID = Column(
        Integer,
        ForeignKey("roles.RoleID"),
        nullable=False
    )