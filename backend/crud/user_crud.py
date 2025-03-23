from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from schemas import UserCreate, UserUpdate
from authorization.auth import hash_password

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
        return {"message": "Successfully created a user. Go to the login page and log in to your new account."}
    
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
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_fields = []  # Lista do przechowywania zaktualizowanych pól

    if user_update.email:
        user.email = user_update.email
        updated_fields.append("email")
    if user_update.password:
        user.password = hash_password(user_update.password)
        updated_fields.append("password")

    if updated_fields:
        db.commit()
        db.refresh(user)
        
        message = "Updated: "
        message += ", ".join(updated_fields)
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail="No data provided for update")