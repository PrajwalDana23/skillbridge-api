from fastapi import FastAPI
from src.db.database import Base, engine
from src.api import batch_routes

import src.models.user  # VERY IMPORTANT
import src.models.batch
from src.api import batch_routes, session_routes, attendance_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "SkillBridge API running"}

from sqlalchemy.orm import Session
from src.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from src.api import auth_routes

app.include_router(auth_routes.router)
app.include_router(batch_routes.router)
app.include_router(batch_routes.router)
app.include_router(session_routes.router)
app.include_router(attendance_routes.router)

import src.models.batch_invite

from src.api import monitoring_routes
from src.api import summary_routes

app.include_router(summary_routes.router)
app.include_router(monitoring_routes.router)