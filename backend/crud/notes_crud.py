from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Note
from schemas import NoteCreate, NoteUpdate
from crud.auth_crud import check_api_key_permissions

# Funkcja do wyświetlania wszystkich notatek dla konkretnego użytkownika
def get_notes(db: Session, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Pobieramy notatki powiązane z użytkownikiem
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found for this user")
    
    return notes

# Funkcja do pobrania szczegółów notatki dla jednego użytkownika
def get_note(db: Session, note_id: int, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Pobieramy notatkę tylko dla danego użytkownika
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or does not belong to this user")
    
    return note

# Funkcja do stworzenia notatki
def create_note(db: Session, note: NoteCreate, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Tworzymy nową notatkę
    db_note = Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return db_note

# Funkcja do aktualizacji notatki
def update_note(db: Session, note_id: int, user_id: int, api_key: str, note_update: NoteUpdate):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this note")

    updated = False  # Flaga informująca, czy coś zostało zmienione

    if note_update.title is not None:
        note.title = note_update.title
        updated = True
    if note_update.content is not None:
        note.content = note_update.content
        updated = True

    if updated:
        db.commit()
        db.refresh(note)
        return {"message": "Note updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="No data provided for update")

# Funkcja do usunięcia notatki
def delete_note(db: Session, note_id: int, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this note")

    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted"}

