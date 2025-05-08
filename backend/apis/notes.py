from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
import crud.notes_crud as crud
import schemas
from schemas import NoteUpdateResponse
from apis.dependencies import get_db
from typing import List


router = APIRouter()

# Endpoint do pobierania wszystkich notatek dla konkretnego użytkownika
@router.get("/notes/", response_model=List[schemas.Note])
def get_all_notes(user_id: int = Query(...), api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.get_notes(db, user_id=user_id, api_key=api_key)

# Endpoint do pobierania jednej notatki dla konkretnego użytkownika
@router.get("/notes/{id}", response_model=schemas.Note)
def get_note(id: int, api_key: str, user_id: int = Query(...), db: Session = Depends(get_db)):
    # Pobieramy notatkę dla konkretnego użytkownika
    return crud.get_note(db, note_id=id, user_id=user_id, api_key=api_key)

# Endpoint do dodawania nowej notatki dla konkretnego użytkownika
@router.post("/notes/", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, user_id: int = Query(...), api_key: str = Query(...), db: Session = Depends(get_db)):
    # Wywołanie funkcji do stworzenia notatki
    return crud.create_note(db, note=note, user_id=user_id, api_key=api_key)

# Endpoint do aktualizacji notatki dla konkretnego użytkownika
@router.put("/notes/{id}", response_model=NoteUpdateResponse)
def update_note(id: int, note_update: schemas.NoteUpdate, user_id: int = Query(...), api_key: str = Query(...), db: Session = Depends(get_db)):
    return crud.update_note(db, note_id=id, user_id=user_id, api_key=api_key, note_update=note_update)

# Endpoint do usunięcia notatki dla konkretnego użytkownika
@router.delete("/notes/{id}", response_model=schemas.NoteUpdateResponse)
def delete_note_endpoint(id: int, user_id: int = Query(...), api_key: str = Query(...), db: Session = Depends(get_db)):
    return crud.delete_note(db, note_id=id, user_id=user_id, api_key=api_key)
