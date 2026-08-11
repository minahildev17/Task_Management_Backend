from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey
)

from database import Base


class User(Base):

    __tablename__ = "users"

    UserID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    Name = Column(
        String(100),
        nullable=False
    )

    Email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    Password = Column(
        String(255),
        nullable=False
    )

    Date_of_birth = Column(
        Date,
        nullable=True
    )

    RoleID = Column(
        Integer,
        ForeignKey("roles.RoleID"),
        nullable=False,
        default=2
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