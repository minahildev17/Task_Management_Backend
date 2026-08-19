from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from models.task import TaskStatus


class TaskCreate(BaseModel):
    ProjectID: int
    Title: str
    Description: str | None = None
    Priority: str = "Medium"
    DueDate: date | None = None
    AssignedTo: int | None = None


class TaskUpdate(BaseModel):
    Title: str | None = None
    Description: str | None = None
    Status: TaskStatus | None = None
    Priority: str | None = None
    DueDate: date | None = None


class TaskAssign(BaseModel):
    UserID: int


class TaskResponse(BaseModel):
    TaskID: int
    ProjectID: int
    AssignedTo: int | None
    CreatedBy: int
    Title: str
    Description: str | None
    Status: TaskStatus
    Priority: str
    DueDate: date | None
    CreatedAt: datetime
    UpdatedAt: datetime

    model_config = ConfigDict(
        from_attributes=True
    )