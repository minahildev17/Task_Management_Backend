from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from models.attachment import Attachment
from models.task import Task

from schemas.attachment_schema import AttachmentResponse

from utils.security import get_current_user
from services.minio_service import upload_file_to_minio


router = APIRouter(
    prefix="/tasks",
    tags=["Ticket Attachments"]
)


# --------------------------------------------------
# ATTACH IMAGE TO TICKET
# --------------------------------------------------

@router.post(
    "/{task_id}/attachments",
    response_model=AttachmentResponse
)
def attach_image(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user_id = int(current_user)

    # Check if ticket exists
    task = db.query(Task).filter(
        Task.TaskID == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Only allow image files
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image attachments are allowed"
        )

    try:
        # Read image file
        file_data = file.file.read()

        # Upload image to MinIO
        file_url = upload_file_to_minio(
            file_data=file_data,
            file_name=file.filename,
            content_type=file.content_type
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload image to MinIO"
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