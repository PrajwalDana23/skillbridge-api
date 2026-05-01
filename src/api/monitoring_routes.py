from fastapi import APIRouter, Depends, HTTPException
import os
from src.core.auth import require_role, create_monitoring_token

router = APIRouter()

@router.post("/auth/monitoring-token")
def get_monitoring_token(api_key: str,
                         user=Depends(require_role(["monitoring_officer"]))):
    # extra layer
    if api_key != os.getenv("MONITORING_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    token = create_monitoring_token({
        "role": "monitoring_officer",
        "user_id": user["user_id"]
    })

    return {"access_token": token}

from fastapi import Request
from jose import jwt
from src.db.database import SessionLocal
from src.models.attendance import Attendance

@router.get("/monitoring/attendance")
def monitoring_attendance(request: Request):
    db = SessionLocal()

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

        # 🔴 CRITICAL CHECKS
        if payload.get("role") != "monitoring_officer":
            raise HTTPException(status_code=403, detail="Forbidden")

        if payload.get("scope") != "monitoring":
            raise HTTPException(status_code=401, detail="Invalid token scope")

    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    data = db.query(Attendance).all()
    return data