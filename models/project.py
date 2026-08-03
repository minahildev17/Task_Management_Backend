from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
)

from database import Base


class Project(Base):
    __tablename__ = "projects"

    ProjectID = Column(Integer, primary_key=True, index=True)

    OrganizationID = Column(
        Integer,
        ForeignKey("organizations.OrganizationID"),
        nullable=False
    )

    CreatedBy = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    Name = Column(String(100), nullable=False)

    Description = Column(
        String(255),
        nullable=True
    )

    Status = Column(
        String(50),
        nullable=False,
        default="Active"
    )

    StartDate = Column(Date, nullable=True)

    EndDate = Column(Date, nullable=True)

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