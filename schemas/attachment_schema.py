from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentCreate(BaseModel):
    FileName: str
    FileType: str


class AttachmentResponse(BaseModel):
    AttachmentID: int
    TaskID: int
    UploadedBy: int
    FileName: str
    FileType: str
    FileURL: str
    CreatedAt: datetime
    UpdatedAt: datetime

    model_config = ConfigDict(
        from_attributes=True
    )