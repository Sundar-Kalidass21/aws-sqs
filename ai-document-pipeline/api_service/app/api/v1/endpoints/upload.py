from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.database import get_db
from shared.models import Job
from shared.schemas import JobMessage, JobResponse
from api_service.app.services.sqs_producer import sqs_client
import shutil
import os
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=JobResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # 1. Save File
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Create Job in DB
        job = Job(filename=file.filename, status="PENDING")
        db.add(job)
        db.commit()
        db.refresh(job)

        # 3. Send to SQS
        message = JobMessage(job_id=job.id, file_path=file_path)
        sqs_client.send_message(message.model_dump())

        return job

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
