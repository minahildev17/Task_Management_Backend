from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    AttachmentID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    TaskID = Column(
        Integer,
        ForeignKey("tasks.TaskID"),
        nullable=False
    )

    UploadedBy = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    FileName = Column(
        String(255),
        nullable=False
    )

    FileType = Column(
        String(100),
        nullable=False
    )

    # AWS S3 image URL will be stored here
    FileURL = Column(
        String(1000),
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