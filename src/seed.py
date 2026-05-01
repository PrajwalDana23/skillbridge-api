from src.db.database import SessionLocal
from src.models.user import User
from src.core.auth import hash_password

db = SessionLocal()

def seed():
    users = [
        User(
            name="Trainer",
            email="trainer@example.com",
            password=hash_password("123456"),
            role="trainer"
        ),
        User(
            name="Student",
            email="student@example.com",
            password=hash_password("123456"),
            role="student"
        ),
        User(
            name="Manager",
            email="pm@example.com",
            password=hash_password("123456"),
            role="programme_manager"
        ),
        User(
            name="Monitor",
            email="mo@example.com",
            password=hash_password("123456"),
            role="monitoring_officer"
        )
    ]

    for u in users:
        existing = db.query(User).filter(User.email == u.email).first()
        if not existing:
            db.add(u)

    db.commit()
    print("Seed data inserted successfully!")

if __name__ == "__main__":
    seed()