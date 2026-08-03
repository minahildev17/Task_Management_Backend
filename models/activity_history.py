from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class ActivityHistory(Base):
    __tablename__ = "activity_history"

    ActivityID = Column(Integer, primary_key=True, index=True)

    UserID = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    TaskID = Column(
        Integer,
        ForeignKey("tasks.TaskID"),
        nullable=True
    )

    Activity = Column(
        String(255),
        nullable=False
    )

    ActivityDate = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )