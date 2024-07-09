import base64
import cv2
import models

def upload_image(id,inpt,oupt,db):
    try:
        new_image = models.FabricImage(history_id=id, input_image=inpt, output_image=oupt)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return True
    except:
        return False


def setData(date, status, file, inputf, output, db):
    try:
        new_fabric = models.Fabric(date=date, status=status, file=file)
        db.add(new_fabric)
        db.commit()
        db.refresh(new_fabric)
        return True, new_fabric.id
    except:
        return False
    

def getHistory(db):

    full_history = db.query(models.Fabric)
    total = full_history.count()
    no_defective = full_history.filter(models.Fabric.status == False).count()
    try:
        accuray = round((no_defective/total)*100,2)
    except:
        accuray=0
    table = full_history.all()
    
    data = {
        "accuracy": accuray,
        "history": table
    }

    return data

def getHistoryId(id, db):
    data = db.query(models.FabricImage).filter(models.FabricImage.history_id == id).first()
    return data

def getProductById(id, db):
    data = db.query(models.Fabric).filter(models.Fabric.id == id).first()
    return data
