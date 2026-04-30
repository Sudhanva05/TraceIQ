from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models

router = APIRouter(prefix="/stats")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/log-levels")
def get_log_levels(db: Session = Depends(get_db)):
    result = (
        db.query(models.Log.log_level, func.count(models.Log.id))
        .group_by(models.Log.log_level)
        .all()
    )

    return {level: count for level, count in result}