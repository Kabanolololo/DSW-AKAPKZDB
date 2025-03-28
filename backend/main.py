from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from apis.notes import router as notes_router
from apis.users import router as users_router
from apis.authorization import router as login_router
from database import SessionLocal, engine
import models as models

# Tworzymy tabele w bazie danych
models.Base.metadata.create_all(bind=engine)

# Tworzymy aplikację FastAPI
app = FastAPI()

# Dodajemy middleware CORS
origins = [
    "http://localhost:8081",  
    "http://127.0.0.1:8081",
    "http://localhost:8080",
    "http://127.0.01:8080" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Rejestrujemy routers dla użytkowników i notatek
app.include_router(users_router)
app.include_router(notes_router)
app.include_router(login_router)
