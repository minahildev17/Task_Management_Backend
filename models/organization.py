from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class Organization(Base):
    __tablename__ = "organizations"

    OrganizationID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    Name = Column(
        String(100),
        nullable=False
    )

    Email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    ContactNo = Column(
        String(20),
        nullable=False
    )

    # Uploaded logo file ka path save hoga
    LogoURL = Column(
        String(500),
        nullable=True
    )

    # Theme table ki Foreign Key
    ThemeID = Column(
        Integer,
        ForeignKey("themes.ThemeID"),
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