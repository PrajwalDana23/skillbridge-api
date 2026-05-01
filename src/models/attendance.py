from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.db.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    student_id = Column(Integer)
    status = Column(String)
    marked_at = Column(DateTime, default=datetime.utcnow)