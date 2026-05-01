from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta
from src.db.database import Base

class BatchInvite(Base):
    __tablename__ = "batch_invites"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    token = Column(String, unique=True)
    created_by = Column(Integer)
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)