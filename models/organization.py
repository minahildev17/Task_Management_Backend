from datetime import datetime
import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base


class ThemeEnum(str, enum.Enum):
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"


class Organization(Base):
    __tablename__ = "organizations"

    OrganizationID = Column(Integer, primary_key=True, index=True)

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

    Theme = Column(
    Enum(ThemeEnum, name="theme_enum"),
    default=ThemeEnum.LIGHT,
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