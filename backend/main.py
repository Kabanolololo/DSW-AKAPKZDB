from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database import SessionLocal, engine
import models
import crud
import schemas

# Tworzymy tabele w bazie danych
models.Base.metadata.create_all(bind=engine)

# Tworzymy aplikację FastAPI
app = FastAPI()

# Funkcja do uzyskania sesji bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint do tworzenia użytkownika
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Wywołanie funkcji do tworzenia użytkownika z `crud.py`
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )