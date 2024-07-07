import models
def setData(date, status, file, db):
    try:
        new_fabric = models.Fabric(date=date, status=status, file=file)
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
    # defective = full_history.filter(models.Fabric.status == True).count()

    accuray = (no_defective/total)*100
    
    data = {
        "accuracy": accuray,
        "history": full_history.all()
    }

    return data
