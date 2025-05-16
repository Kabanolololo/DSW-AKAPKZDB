from fastapi import APIRouter, Depends, Query, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from apis.dependencies import get_db
from datetime import datetime
from crud.API_Key_crud import check_api_key_permissions

router = APIRouter()

# Endpoint służacy do pingowania 
@router.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# Endpoint służacy do eksportu tabel dla local db
@router.get("/export_data")
def export_data(
    user_id: int = Query(..., description="User Id"),
    db: Session = Depends(get_db),
    api_key: str = Header(...)
):
    try:
        check_api_key_permissions(db, api_key, user_id)
        def serialize_row(row):
            return {
                key: (value.isoformat() if isinstance(value, datetime) else value)
                for key, value in row._mapping.items()
            }

        def run_query(query: str, params: dict = {}):
            result = db.execute(text(query), params)
            return [serialize_row(row) for row in result.fetchall()]

        users = run_query("SELECT id, nick, email FROM users WHERE id = :user_id", {"user_id": user_id})
        notes = run_query("SELECT * FROM notes WHERE user_id = :user_id", {"user_id": user_id})

        # Pobieramy tylko te tagi, które są powiązane z notatkami użytkownika
        tags = run_query("""
            SELECT * FROM tags 
            WHERE note_id IN (
                SELECT id FROM notes WHERE user_id = :user_id
            )
        """, {"user_id": user_id})

        return JSONResponse(
            content={
                "users": users,
                "notes": notes,
                "tags": tags,
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)