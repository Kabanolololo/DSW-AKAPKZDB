from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import crud
import schemas
from apis.dependencies import get_db
from typing import List


router = APIRouter()

# Endpoint do pobierania wszystkich notatek dla konkretnego użytkownika
@router.get("/notes/", response_model=List[schemas.Note])
def get_all_notes(user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.get_notes(db, user_id=user_id)

# Endpoint do pobierania jednej notatki dla konkretnego użytkownika
@router.get("/notes/{id}", response_model=schemas.Note)
def get_note(id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.get_note(db, note_id=id, user_id=user_id)

# Endpoint do dodawania nowej notatki dla konkretnego użytkownika
@router.post("/notes/", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.create_note(db, note=note, user_id=user_id)

# Endpoint do aktualizacji notatki dla konkretnego użytkownika
@router.put("/notes/{id}", response_model=schemas.Note)
def update_note(id: int, note_update: schemas.NoteUpdate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.update_note(db, note_id=id, user_id=user_id, note_update=note_update)

# Endpoint do usunięcia notatki dla konkretnego użytkownika
@router.delete("/notes/{id}")
def delete_note(id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.delete_note(db, note_id=id, user_id=user_id)