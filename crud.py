from fastapi import APIRouter, Depends, HTTPException, UploadFile
import service
from database import engine, get_db
from sqlalchemy.orm import Session
from datetime import datetime

fabric_router = APIRouter(prefix="/fabric/api/v1", tags=["Fabric"])

@fabric_router.post("/isdefective")
def is_defective(file: UploadFile, db: Session = Depends(get_db)):
    date = datetime.now()
    status = True #get from ml models
    add_db = service.setData(date=date, status=status, file=file.filename, db=db)
    if add_db:
        return {"status": status, "date": date, "file": file.filename}
    else:
        return HTTPException(status_code=505, detail="DB error")

@fabric_router.get("/productionhistory")
def production_history(db: Session = Depends(get_db)):
    return service.getHistory(db=db)