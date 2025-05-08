# Projekt API

## Opis
Jest to API do zarządzania użytkownikami i notatkami, stworzone przy użyciu **FastAPI**. API pozwala na rejestrację użytkowników, logowanie oraz zarządzanie notatkami.

## Technologie
- **FastAPI** - Framework do budowy API.
- **SQLAlchemy** - ORM do interakcji z bazą danych.
- **Pydantic** - Walidacja danych.
- **PostgreSQL** (lub inna baza danych) - Baza danych do przechowywania danych.
- **Python 3.7+**

## Instalacja

### Krok 1: Sklonuj repozytorium
Najpierw sklonuj repozytorium na swoje lokalne urządzenie:

```bash
git clone https://github.com/Kabanolololo/DSW-AKAPKZDB
cd DSW-AKAPKZDB
```
### Krok 1: Utwórz wirtualne środowisko
Utwórz nowe wirtualne środowisko, aby zainstalować wszystkie zależności:

```bash
python -m venv venv
```

### Krok 2: Aktywuj wirtualne środowisko
Wszystko zależy od tego czy używamy Windowsa czy Linuxa
### Krok 3: Zainstaluj zależności
Zainstaluj wszystkie wymagane zależności z pliku `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Krok 4: Uruchom aplikację
Uruchom serwer aplikacji za pomocą Uvicorn:

```bash
uvicorn main:app --reload
```

Gdzie:
- `main` to plik, w którym znajduje się aplikacja FastAPI (np. `main.py`).
- `app` to obiekt aplikacji FastAPI.

Po uruchomieniu aplikacji, będzie ona dostępna pod adresem:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

Dodatkowo, dokumentacja interaktywna API będzie dostępna pod:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Podsumowanie
Użyj `uvicorn` do uruchomienia aplikacji. API będzie dostępne pod lokalnym adresem [http://127.0.0.1:8000](http://127.0.0.1:8000). Możesz uzyskać dostęp do interaktywnej dokumentacji API pod adresem [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
