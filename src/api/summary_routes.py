from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.batch_student import BatchStudent
from src.models.session import Session as SessionModel
from src.models.attendance import Attendance
from src.core.auth import require_role
from src.dependencies import get_current_user

router = APIRouter(prefix="/programme")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def programme_summary(user=Depends(get_current_user)):
    return {"message": "Programme summary"}

@router.get("/batches/{batch_id}/summary")
def batch_summary(batch_id: int,
                  db: Session = Depends(get_db),
                  user=Depends(require_role(["institution"]))):

    students = db.query(BatchStudent).filter_by(batch_id=batch_id).count()
    sessions = db.query(SessionModel).filter_by(batch_id=batch_id).count()

    attendance_records = db.query(Attendance).join(
        SessionModel, Attendance.session_id == SessionModel.id
    ).filter(SessionModel.batch_id == batch_id).count()

    return {
        "batch_id": batch_id,
        "total_students": students,
        "total_sessions": sessions,
        "attendance_records": attendance_records
    }
from fastapi import HTTPException

@router.get("/institutions/{institution_id}/summary")
def institution_summary(institution_id: int,
                        db: Session = Depends(get_db),
                        user=Depends(require_role(["programme_manager"]))):

    # 🔍 Validate institution exists via batches (since no separate table)
    batches = db.query(Batch).filter_by(institution_id=institution_id).all()

    if not batches:
        raise HTTPException(status_code=404, detail="Institution not found")

    batch_ids = [b.id for b in batches]

    total_batches = len(batch_ids)

    total_students = db.query(BatchStudent).filter(
        BatchStudent.batch_id.in_(batch_ids)
    ).count()

    total_sessions = db.query(SessionModel).filter(
        SessionModel.batch_id.in_(batch_ids)
    ).count()

    total_attendance = db.query(Attendance).join(
        SessionModel, Attendance.session_id == SessionModel.id
    ).filter(
        SessionModel.batch_id.in_(batch_ids)
    ).count()

    return {
        "institution_id": institution_id,
        "total_batches": total_batches,
        "total_students": total_students,
        "total_sessions": total_sessions,
        "attendance_records": total_attendance
    }