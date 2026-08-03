from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Organization(Base):
    __tablename__ = "organizations"

    OrganizationID = Column(Integer, primary_key=True, index=True)

    Name = Column(String(100), nullable=False)

    Email = Column(String(100), unique=True, nullable=False)

    ContactNo = Column(String(20), nullable=False)

    Logo = Column(String(255), nullable=True)

    Theme = Column(String(100), nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    UpdatedAt = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )