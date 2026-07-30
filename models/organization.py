from sqlalchemy import Column, Integer, String
from database import Base


class Organization(Base):
    __tablename__ = "organizations"

    OrganizationID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    ContactNo = Column(String(20), nullable=False)