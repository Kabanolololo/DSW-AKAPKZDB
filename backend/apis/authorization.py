from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserLogin, LogoutRequest
from models import User
from models import ApiKey
from apis.dependencies import get_db
from authorization.auth import hash_password_sha256,generate_api_key

router = APIRouter()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Sprawdzamy, czy użytkownik istnieje w bazie danych
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Jeżeli użytkownik nie istnieje lub hasło jest niepoprawne
    if not db_user or hash_password_sha256(user.password) != db_user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password or username"
        )

    # Sprawdzamy, czy użytkownik ma już API Key
    api_key = db.query(ApiKey).filter(ApiKey.user_id == db_user.id).first()
    
    if not api_key:
        new_api_key = generate_api_key()
        api_key = ApiKey(key=new_api_key, user_id=db_user.id)
        db.add(api_key)
        db.commit()
        db.refresh(api_key)

    # Zwracamy zarówno API Key, jak i dane użytkownika
    return {
        "api_key": api_key.key,
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "nick": db_user.nick
        }
    }

@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    # Sprawdzamy, czy klucz API istnieje w bazie
    db_api_key = db.query(ApiKey).filter(ApiKey.key == request.api_key).first()
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    # Usuwamy klucz API
    db.delete(db_api_key)
    db.commit()

    return {"message": "Successfully logged out"}

