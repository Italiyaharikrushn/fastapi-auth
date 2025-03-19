import uuid
import shutil
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from db.session import get_db
from models.document import Document

router = APIRouter()

UPLOAD_DIR = "static/images/"  # Image store karva mate directory

@router.post("/upload-image/")
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"{UPLOAD_DIR}{unique_filename}"

    # Save file to static/images
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save image path in the database
    document = Document(static_file_path=file_path)
    db.add(document)
    db.commit()
    db.refresh(document)

    return {"file_id": document.id, "file_url": file_path}
