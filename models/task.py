from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    TaskID = Column(Integer, primary_key=True, index=True)

    ProjectID = Column(
        Integer,
        ForeignKey("projects.ProjectID"),
        nullable=False
    )

    AssignedTo = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    CreatedBy = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    Title = Column(String(100), nullable=False)

    Description = Column(
        String(255),
        nullable=True
    )

    Status = Column(
        String(50),
        nullable=False,
        default="Pending"
    )

    Priority = Column(
        String(50),
        nullable=False,
        default="Medium"
    )

    DueDate = Column(
        Date,
        nullable=True
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