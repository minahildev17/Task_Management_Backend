from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from database import Base


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    OrganizationMemberID = Column(
        Integer,
        primary_key=True,
        index=True
    )

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

    CreatedAt = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    UpdatedAt = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )