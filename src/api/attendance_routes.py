from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_current_user

router = APIRouter()

@router.post("/attendance/mark")   # ✅ FIXED PATH
def mark_attendance(
    session_id: int,
    status: str,
    user=Depends(get_current_user)
):

    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    return {
        "message": "Attendance marked",
        "session_id": session_id,
        "status": status
    }