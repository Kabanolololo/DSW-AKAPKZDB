from fastapi import FastAPI, Depends, HTTPException, status
from apis.users import router as users_router
from apis.notes import router as notes_router
from database import SessionLocal, engine
import models as models

# Tworzymy tabele w bazie danych
models.Base.metadata.create_all(bind=engine)

# Tworzymy aplikację FastAPI
app = FastAPI()

app.include_router(users_router)
app.include_router(notes_router)
