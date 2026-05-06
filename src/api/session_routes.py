from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_current_user

router = APIRouter()   # ✅ REQUIRED
@router.post("/sessions")
def create_session(user=Depends(get_current_user)):

    if user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers allowed")

    return {"message": "Session created"}