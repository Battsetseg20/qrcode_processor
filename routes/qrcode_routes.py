# /routes/qrcode_routes.py
import os
import re

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

import crud_operations
from main import get_db
from security import get_current_user, oauth2_scheme
from services import qrcode_data_service, qrcode_process_service

router = APIRouter()


@router.post("/upload_qr/")
async def upload_qr(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    Upload a QR code image and process the QR code data to update the database. First authenticate the user using the token.
    Format of the QR code data: uuid - username - department_name - role
    """

    # Check if the user exists
    user = crud_operations.get_user_by_username(db, current_user)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # Sanitize the filename
    safe_filename = sanitize_filename(file.filename)

    file_path = f"temp_{safe_filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Call the QR service to read the QR code
    qr_data = qrcode_process_service.read_qr_code(file_path)

    # Close and remove the file
    await file.close()
    os.remove(file_path)

    # Ensure that there are 4 parts in the split QR data.
    parts = qr_data.split(" - ")
    if len(parts) != 4:
        raise HTTPException(status_code=400, detail="Invalid QR data format")

    uuid_code, username, role, department_name = parts

    # Process QR data by calling the QR service
    try:
        response_data = qrcode_data_service.process_qr_data(
            db, uuid_code, username, role, department_name
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing QR code: {e}")

    return {"detail": "QR code processed", "data": response_data}


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r"[^\w\.-]", "_", filename)

    sanitized = sanitized.replace("..", "_")

    return sanitized
