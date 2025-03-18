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

# Endpoint do pobierania szczegółów użytkownika po ID
@app.get("/users/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Endpoint do aktualizacji danych użytkownika
@app.put("/users/{id}", response_model=schemas.User)
def update_user(id: int, user_update: schemas.UserCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id=id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user