from sqlalchemy import Column, Integer, String
from database import Base


class Theme(Base):
    __tablename__ = "themes"

    ThemeID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    Name = Column(
        String(50),
        unique=True,
        nullable=False
    )