import base64
import cv2
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
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

def image_to_base64(image):
    retval, buffer = cv2.imencode('.jpeg', image)
    if retval:
        base64_string = base64.b64encode(buffer).decode('utf-8')
        return base64_string
    else:
        return None

@fabric_router.post("/isdefective")
def is_defective(file: UploadFile = File(...),Fname: str = Form(...), db: Session = Depends(get_db)):
    
    print("*************************************************************")
    print(Fname)
    print(file.filename)
    print("*************************************************************")
    file_name = file.filename
    if(Fname=="none"):
        file_name = file.filename
    else:
        file_name = Fname

        # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Define the file path
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save the file to the local file system
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    original_image = cv2.imread(f"{UPLOAD_DIR}/{file_name}", 0) 

    date = datetime.now()
    figure, status = ml.detect_defects(original_image, autoencoder, treshold)
    # status = True #get from ml models
    add_db, f_id = service.setData(date=date, status=status, file=file_name, inputf=original_image, output=figure , db=db)

    os.remove(file_path)

    # submited_data = service.getHistoryId(id=data_id,db=db)
    ori_img = image_to_base64(original_image)
    re_img = image_to_base64(figure)

    service.upload_image(id=f_id, inpt=ori_img, oupt=re_img, db=db)

    submited_data={
        "date":date,
        "status":status,
        "file":file_name,
        "input_image":ori_img,
        "reconstruct_image":re_img
    }

    if add_db:
        return submited_data
    else:
        return HTTPException(status_code=505, detail="DB error")

@fabric_router.get("/productionhistory")
def production_history(db: Session = Depends(get_db)):
    return service.getHistory(db=db)

@fabric_router.get("/productionhistory/{id}")
def production_history(id: int, db: Session = Depends(get_db)):
    return service.getHistoryId(id=id,db=db)

@fabric_router.get("/getProductById/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return service.getProductById(id=id, db=db)