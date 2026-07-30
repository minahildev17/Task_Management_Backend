from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    Description = Column(String(255))
    StartDate = Column(Date)
    EndDate = Column(Date)