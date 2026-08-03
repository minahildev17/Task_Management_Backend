from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from database import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    ProjectMemberID = Column(Integer, primary_key=True, index=True)

    ProjectID = Column(
        Integer,
        ForeignKey("projects.ProjectID"),
        nullable=False
    )

    UserID = Column(
        Integer,
        ForeignKey("users.UserID"),
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