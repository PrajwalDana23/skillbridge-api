from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.db.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    trainer_id = Column(Integer)
    title = Column(String)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)