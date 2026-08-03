from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from database import Base


class Permission(Base):
    __tablename__ = "permissions"

    PermissionID = Column(Integer, primary_key=True, index=True)

    PermissionName = Column(String(100), nullable=False)

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