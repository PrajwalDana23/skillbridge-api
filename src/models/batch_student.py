from sqlalchemy import Column, Integer
from src.db.database import Base

class BatchStudent(Base):
    __tablename__ = "batch_students"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    student_id = Column(Integer)