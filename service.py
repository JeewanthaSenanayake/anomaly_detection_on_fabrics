import base64
import cv2
import models

def setData(date, status, file, inputf, output, db):
    try:
        new_fabric = models.Fabric(date=date, status=status, file=file.filename)
        db.add(new_fabric)
        db.commit()
        db.refresh(new_fabric)
        return True
    except:
        return False
    

def getHistory(db):

    full_history = db.query(models.Fabric)
    total = full_history.count()
    no_defective = full_history.filter(models.Fabric.status == False).count()
    
    accuray = round((no_defective/total)*100,2)
    table = full_history.all()
    
    data = {
        "accuracy": accuray,
        "history": table
    }

    return data

def getHistoryId(id, db):
    data = db.query(models.Fabric).filter(models.Fabric.id == id).first()
    return data
