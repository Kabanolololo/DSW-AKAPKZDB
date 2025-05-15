from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User, ApiKey
from utils.generate_api_key import generate_api_key
from utils.hash import hash_password_sha256

def login_user(db: Session, email: str, password: str) -> dict:
    # Sprawdź czy użytkownik istnieje
    user = db.query(User).filter(User.email == email).first()
    if not user or hash_password_sha256(password) != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password or username"
        )

    # Szukamy istniejącego API Key
    api_key = db.query(ApiKey).filter(ApiKey.user_id == user.id).first()

    if not api_key:
        new_key = generate_api_key()
        api_key = ApiKey(key=new_key, user_id=user.id)
        db.add(api_key)
        db.commit()
        db.refresh(api_key)

    return {
        "api_key": api_key.key,
        "user": {
            "id": user.id,
            "email": user.email,
            "nick": user.nick
        }
    }

def logout_user(db: Session, api_key: str) -> dict:
    db_key = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    if not db_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    db.delete(db_key)
    db.commit()

    return { "message": "Successfully logged out" }
