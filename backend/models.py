from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    log_level = Column(String(20))
    source_ip = Column(String(50))
    service_name = Column(String(100))
    status_code = Column(Integer, nullable=True)
    message = Column(Text)
    raw_line = Column(Text)