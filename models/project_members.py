from sqlalchemy import Column, Integer, ForeignKey
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