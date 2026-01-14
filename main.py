from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running successfully"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
