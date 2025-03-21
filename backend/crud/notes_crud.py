from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Note
from schemas import NoteCreate, NoteUpdate

# Funkcja do wyświetlania wszystkich notatek dla konkretnego użytkownika
def get_notes(db: Session, user_id: int):
    return db.query(Note).filter(Note.user_id == user_id).all()

# Funkcja do pobrania szczegółów notatki dla jednego użytkownika
def get_note(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or does not belong to this user")
    return note

# Funkcja do stworzenia notatki
def create_note(db: Session, note: NoteCreate, user_id: int):
    db_note = Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Funkcja do zaktualizowania notatki
def update_note(db: Session, note_id: int, user_id: int, note_update: NoteUpdate):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this note")

    note.title = note_update.title
    note.content = note_update.content
    db.commit()
    db.refresh(note)
    return note

# Funkcja do usunięcia notatki
def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this note")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
