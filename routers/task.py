from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task, TaskStatus
from models.project import Project
from models.user import User
from models.attachment import Attachment

from schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskAssign,
    TaskResponse
)

from schemas.attachment_schema import AttachmentResponse

from services.minio_service import upload_file_to_minio

from utils.security import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tickets"]
)


# --------------------------------------------------
# ALLOWED STATUS TRANSITIONS
# --------------------------------------------------

ALLOWED_TRANSITIONS = {
    TaskStatus.READY_TO_DO: {
        TaskStatus.IN_PROGRESS,
        TaskStatus.BLOCKED
    },

    TaskStatus.IN_PROGRESS: {
        TaskStatus.READY_TO_DO,
        TaskStatus.BLOCKED,
        TaskStatus.TESTING
    },

    TaskStatus.BLOCKED: {
        TaskStatus.IN_PROGRESS
    },

    TaskStatus.TESTING: {
        TaskStatus.DONE,
        TaskStatus.IN_PROGRESS
    },

    TaskStatus.DONE: {
        TaskStatus.IN_PROGRESS
    }
}


# --------------------------------------------------
# CREATE TICKET
# --------------------------------------------------

@router.post(
    "/",
    response_model=TaskResponse
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    project = db.query(Project).filter(
        Project.ProjectID == task_data.ProjectID
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if task_data.AssignedTo is not None:

        assigned_user = db.query(User).filter(
            User.UserID == task_data.AssignedTo
        ).first()

        if not assigned_user:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
            )

    task = Task(
        ProjectID=task_data.ProjectID,
        AssignedTo=task_data.AssignedTo,
        CreatedBy=user_id,
        Title=task_data.Title,
        Description=task_data.Description,
        Status=task_data.Status,
        Priority=task_data.Priority,
        DueDate=task_data.DueDate
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# --------------------------------------------------
# UPDATE TICKET
# --------------------------------------------------

@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.TaskID == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    # ----------------------------------------------
    # STATUS TRANSITION VALIDATION
    # ----------------------------------------------

    if "Status" in update_data:

        current_status = task.Status
        new_status = update_data["Status"]

        # Same status is allowed
        if current_status != new_status:

            allowed_statuses = ALLOWED_TRANSITIONS.get(
                current_status,
                set()
            )

            if new_status not in allowed_statuses:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid status transition: "
                        f"{current_status.value} → {new_status.value}"
                    )
                )

    # ----------------------------------------------
    # UPDATE TASK FIELDS
    # ----------------------------------------------

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


# --------------------------------------------------
# DELETE TICKET
# --------------------------------------------------

@router.delete(
    "/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.TaskID == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }


# --------------------------------------------------
# ASSIGN TICKET TO USER
# --------------------------------------------------

@router.put(
    "/{task_id}/assign",
    response_model=TaskResponse
)
def assign_task(
    task_id: int,
    assignment: TaskAssign,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.TaskID == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    user = db.query(User).filter(
        User.UserID == assignment.UserID
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    task.AssignedTo = assignment.UserID

    db.commit()
    db.refresh(task)

    return task


# --------------------------------------------------
# UPLOAD TICKET IMAGE
# --------------------------------------------------

@router.post(
    "/{task_id}/attachments",
    response_model=AttachmentResponse
)
async def upload_ticket_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    # Check ticket exists
    task = db.query(Task).filter(
        Task.TaskID == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Check file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )

    # Read image
    file_data = await file.read()

    if not file_data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Upload image to MinIO
    file_url = upload_file_to_minio(
        file_data=file_data,
        file_name=file.filename,
        content_type=file.content_type
    )

    # Save attachment information in MySQL
    attachment = Attachment(
        TaskID=task_id,
        UploadedBy=user_id,
        FileName=file.filename,
        FileType=file.content_type,
        FileURL=file_url
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment