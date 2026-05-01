from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.session import Session as SessionModel
from src.core.auth import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sessions")
def create_session(batch_id: int,
                   title: str,
                   date: str,
                   start_time: str,
                   end_time: str,
                   db: Session = Depends(get_db),
                   user=Depends(require_role(["trainer"]))):

    session = SessionModel(
        batch_id=batch_id,
        trainer_id=user["user_id"],
        title=title,
        date=date,
        start_time=start_time,
        end_time=end_time
    )

    db.add(session)
    db.commit()

    return {"message": "Session created"}