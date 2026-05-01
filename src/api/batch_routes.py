from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.batch import Batch
from src.core.auth import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/batches")
def create_batch(name: str,
                 institution_id: int,
                 db: Session = Depends(get_db),
                 user=Depends(require_role(["trainer", "institution"]))):

    batch = Batch(name=name, institution_id=institution_id)

    db.add(batch)
    db.commit()
    db.refresh(batch)

    return {"message": "Batch created", "batch_id": batch.id}

from src.models.batch_student import BatchStudent

@router.post("/batches/join")
def join_batch(batch_id: int,
               db: Session = Depends(get_db),
               user=Depends(require_role(["student"]))):

    entry = BatchStudent(batch_id=batch_id, student_id=user["user_id"])

    db.add(entry)
    db.commit()

    return {"message": "Joined batch"}

import uuid
from datetime import datetime, timedelta
from src.models.batch_invite import BatchInvite

@router.post("/batches/{batch_id}/invite")
def create_invite(batch_id: int,
                  db: Session = Depends(get_db),
                  user=Depends(require_role(["trainer"]))):

    token = str(uuid.uuid4())

    invite = BatchInvite(
        batch_id=batch_id,
        token=token,
        created_by=user["user_id"],
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )

    db.add(invite)
    db.commit()

    return {"invite_token": token}

from datetime import datetime
from fastapi import HTTPException
from src.models.batch_invite import BatchInvite
from src.models.batch_student import BatchStudent

@router.post("/batches/join")
def join_batch(token: str,
               db: Session = Depends(get_db),
               user=Depends(require_role(["student"]))):

    invite = db.query(BatchInvite).filter(
        BatchInvite.token == token,
        BatchInvite.used == False
    ).first()

    # ❌ Invalid token
    if not invite:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    # ❌ Expired token
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invite expired")

    # ❌ Already joined (avoid duplicate entry)
    existing = db.query(BatchStudent).filter(
        BatchStudent.batch_id == invite.batch_id,
        BatchStudent.student_id == user["user_id"]
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already joined")

    # ✅ Add student to batch
    entry = BatchStudent(
        batch_id=invite.batch_id,
        student_id=user["user_id"]
    )

    # mark invite used
    invite.used = True

    db.add(entry)
    db.commit()

    return {"message": "Joined batch successfully"}