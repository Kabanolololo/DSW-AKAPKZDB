from sqlalchemy.orm import Session
from models import ApiKey
from fastapi import HTTPException, status

# Funkcja do weryfikowania klucza API
def verify_api_key(db: Session, api_key: str) -> ApiKey:
    # Sprawdzamy, czy klucz API jest prawidłowy
    db_api_key = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    return db_api_key

# Funkcja sprawdzająca, czy API Key jest przypisany do użytkownika
def check_api_key_permissions(db: Session, api_key: str, user_id: int) -> bool:
    db_api_key = verify_api_key(db, api_key)
    
    if db_api_key.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this user"
        )
    
    return True