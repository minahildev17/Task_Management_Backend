from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Comment(Base):
    __tablename__ = "comments"

    CommentID = Column(Integer, primary_key=True, index=True)

    TaskID = Column(
        Integer,
        ForeignKey("tasks.TaskID"),
        nullable=False
    )

    UserID = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    CommentText = Column(String(500), nullable=False)