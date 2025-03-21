from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from schemas import UserCreate
from auth import hash_password

# Funkcja do tworzenia nowego użytkownika
def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        ) from e

# Funkcja do wyświetlania konkretnego użytkownika        
def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Funkcja do aktualizacji użytkownika
def update_user(db: Session, user_id: int, user_update: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = user_update.email
    user.password = user_update.password

    db.commit()
    db.refresh(user)
    return user
