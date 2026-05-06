from fastapi import FastAPI
from src.db.database import Base, engine

# Import models (VERY IMPORTANT for table creation)
import src.models.user
import src.models.batch
import src.models.session
import src.models.attendance
import src.models.batch_invite

# Import routers
from src.api import auth_routes
from src.api import batch_routes
from src.api import session_routes
from src.api import attendance_routes
from src.api import monitoring_routes
from src.api import summary_routes
from src.api.protected_routes import router as protected_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "SkillBridge API running"}

# Register routers
app.include_router(auth_routes.router)
app.include_router(batch_routes.router)
app.include_router(session_routes.router)
app.include_router(attendance_routes.router)
app.include_router(summary_routes.router)
app.include_router(monitoring_routes.router)
app.include_router(protected_router)