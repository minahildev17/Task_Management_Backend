from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    Description = Column(String(255))
    Status = Column(String(50), nullable=False)
    Priority = Column(String(50), nullable=False)
    DueDate = Column(Date)