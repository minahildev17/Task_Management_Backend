from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    AttachmentID = Column(Integer, primary_key=True, index=True)

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

    FileName = Column(String(255), nullable=False)
    FilePath = Column(String(500), nullable=False)