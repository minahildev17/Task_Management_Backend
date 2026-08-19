from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum as SQLEnum
from database import Base


class TaskStatus(str, Enum):
    READY_TO_DO = "Ready to Do"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    TESTING = "Testing"
    DONE = "Done"


class Task(Base):
    __tablename__ = "tasks"

    TaskID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ProjectID = Column(
        Integer,
        ForeignKey("projects.ProjectID"),
        nullable=False
    )

    # Ticket baad mein kisi user ko assign kiya ja sakta hai
    AssignedTo = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=True
    )

    CreatedBy = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    Title = Column(
        String(100),
        nullable=False
    )

    Description = Column(
        String(255),
        nullable=True
    )

    Status = Column(
        SQLEnum(TaskStatus),
        nullable=False,
        default=TaskStatus.READY_TO_DO
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