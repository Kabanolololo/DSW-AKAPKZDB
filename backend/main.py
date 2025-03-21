from fastapi import FastAPI, Depends, HTTPException, status, Query
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

# Endpoint do pobierania wszystkich notatek dla konkretnego użytkownika
@app.get("/notes/", response_model=List[schemas.Note])
def get_all_notes(user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.get_notes(db, user_id=user_id)

# Endpoint do pobierania jednej notatki dla konkretnego użytkownika
@app.get("/notes/{id}", response_model=schemas.Note)
def get_note(id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.get_note(db, note_id=id, user_id=user_id)

# Endpoint do dodawania nowej notatki dla konkretnego użytkownika
@app.post("/notes/", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.create_note(db, note=note, user_id=user_id)

# Endpoint do aktualizacji notatki dla konkretnego użytkownika
@app.put("/notes/{id}", response_model=schemas.Note)
def update_note(id: int, note_update: schemas.NoteUpdate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.update_note(db, note_id=id, user_id=user_id, note_update=note_update)

# Endpoint do usunięcia notatki dla konkretnego użytkownika
@app.delete("/notes/{id}")
def delete_note(id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.delete_note(db, note_id=id, user_id=user_id)