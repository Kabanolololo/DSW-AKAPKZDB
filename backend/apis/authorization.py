from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.auth_schema import UserLogin, LogoutRequest
from apis.dependencies import get_db
from crud.authorization_crud import login_user,logout_user

router = APIRouter()

# Endpoint służacy do logowania
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, email=user.email, password=user.password)

# Endpoint służacy do wylogowania
@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    return logout_user(db, api_key=request.api_key)
