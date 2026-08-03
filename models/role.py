from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Role(Base):
    __tablename__ = "roles"

    RoleID = Column(Integer, primary_key=True, index=True)

    RoleName = Column(String(50), nullable=False, unique=True)

    Description = Column(String(255), nullable=True)

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