from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.db.database import SessionLocal
from src.models.user import User
from src.schemas import SignupRequest, LoginRequest
from src.auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/auth/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
     db.delete(existing)
     db.commit()

    new_user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_token({"user_id": new_user.id, "role": new_user.role})
    return {"access_token": token}

@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    # ✅ AUTO CREATE USER IF NOT EXISTS
    if not user:
        user = User(
            name="Auto User",
            email=data.email,
            hashed_password=hash_password(data.password),
            role="student" if "student" in data.email else "trainer"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id, "role": user.role})

    return {"access_token": token}