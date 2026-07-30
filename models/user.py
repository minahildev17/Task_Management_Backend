from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    UserID = Column(Integer, primary_key=True, index=True)
    OrganizationID = Column(Integer, ForeignKey("organizations.OrganizationID"))

    Name = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Date_of_birth = Column(Date)