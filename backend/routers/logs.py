from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import re
from datetime import datetime

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.Log).limit(50).all()

    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "log_level": log.log_level,
            "service": log.service_name,
            "message": log.message
        }
        for log in logs
    ]

@router.post("/upload-log")
async def upload_log(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    lines = content.decode("utf-8").split("\n")

    count = 0

    pattern = r"\[(.*?)\]\s+(DEBUG|INFO|ERROR)\s+-\s+\[(.*?)\]\s+(.*)"

    for line in lines:
        if line.strip() == "":
            continue

        match = re.match(pattern, line)

        if match:
            timestamp_str, log_level, thread, message = match.groups()

            # Convert timestamp
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
            except:
                timestamp = None

            log = models.Log(
                timestamp=timestamp,
                log_level=log_level,
                service_name=thread,
                message=message,
                raw_line=line
            )
        else:
            # fallback if pattern fails
             continue
            
        db.add(log)
        count += 1

    db.commit()

    return {"message": f"{count} log lines inserted"}