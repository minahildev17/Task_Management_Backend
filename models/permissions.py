from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Permission(Base):
    __tablename__ = "permissions"

    PermissionID = Column(Integer, primary_key=True, index=True)
    PermissionName = Column(String(100), nullable=False)
    RoleID = Column(Integer, ForeignKey("roles.RoleID"))