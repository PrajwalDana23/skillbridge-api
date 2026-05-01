from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.attendance import Attendance
from src.models.batch_student import BatchStudent
from src.core.auth import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/attendance/mark")
def mark_attendance(session_id: int,
                    status: str,
                    db: Session = Depends(get_db),
                    user=Depends(require_role(["student"]))):

    # check if student belongs to batch
    enrolled = db.query(BatchStudent).filter(
        BatchStudent.student_id == user["user_id"]
    ).first()

    if not enrolled:
        raise HTTPException(status_code=403, detail="Not enrolled")

    attendance = Attendance(
        session_id=session_id,
        student_id=user["user_id"],
        status=status
    )

    db.add(attendance)
    db.commit()

    return {"message": "Attendance marked"}