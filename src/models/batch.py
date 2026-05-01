from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.db.database import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    institution_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)