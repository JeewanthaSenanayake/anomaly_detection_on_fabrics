import cv2
from fastapi import APIRouter, Depends, HTTPException, UploadFile
import service
from database import engine, get_db
from sqlalchemy.orm import Session
from datetime import datetime
import ML_Model.executionFile as ml
import os
import shutil

autoencoder = ml.generate_AE()
treshold = 0.18039123161949278
UPLOAD_DIR = "uploaded_images"

fabric_router = APIRouter(prefix="/fabric/api/v1", tags=["Fabric"])

@fabric_router.post("/isdefective")
def is_defective(file: UploadFile, db: Session = Depends(get_db)):
        # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Define the file path
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file to the local file system
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    original_image = cv2.imread(f"{UPLOAD_DIR}/{file.filename}", 0) 

    date = datetime.now()
    figure, status = ml.detect_defects(original_image, autoencoder, treshold)
    # status = True #get from ml models
    add_db = service.setData(date=date, status=status, file=file.filename, db=db)

    os.remove(file_path)

    if add_db:
        return {"status": status, "date": date, "file": file.filename}
    else:
        return HTTPException(status_code=505, detail="DB error")

@fabric_router.get("/productionhistory")
def production_history(db: Session = Depends(get_db)):
    return service.getHistory(db=db)