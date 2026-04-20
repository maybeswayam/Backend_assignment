from fastapi import APIRouter, Depends, Query, HTTPException
from app.reading.schemas import BookmarkCreate, NoteCreate
from app.auth.utils import get_current_user
from app.database import supabase
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/bookmarks")
def add_bookmark(b: BookmarkCreate, user: dict = Depends(get_current_user)):
    data = {
        "id": str(uuid.uuid4()),
        "user_id": user['id'],
        "ebook_id": b.ebook_id,
        "page_number": b.page_number,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        db_res = supabase.table("bookmarks").insert(data).execute()
        return db_res.data
    except Exception as e:
        # checking specifically for foreign key violation
        if '23503' in str(e):
            raise HTTPException(status_code=400, detail="Invalid ebook ID")
        raise HTTPException(status_code=500, detail="Could not save bookmark, please try again")

@router.get("/bookmarks")
def get_bookmarks(ebook_id: str = Query(...), user: dict = Depends(get_current_user)):
    try:
        res = supabase.table("bookmarks").select("*").eq("user_id", user["id"]).eq("ebook_id", ebook_id).execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to load bookmarks")

@router.delete('/bookmarks/{bookmark_id}')
def remove_bookmark(bookmark_id: str, user: dict = Depends(get_current_user)):
    try:
        supabase.table("bookmarks").delete().eq("user_id", user["id"]).eq("id", bookmark_id).execute()
        return {"status": "deleted"}
    except Exception:
        raise HTTPException(status_code=500, detail="Could not remove bookmark")

@router.post("/notes")
def add_note(n: NoteCreate, user: dict = Depends(get_current_user)):
    data = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "ebook_id": n.ebook_id,
        "page_number": n.page_number,
        "content": n.content,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        res = supabase.table("notes").insert(data).execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Could not save note")

@router.get('/notes')
def get_notes(ebook_id: str = Query(...), user: dict = Depends(get_current_user)):
    # TODO: maybe let users search within their own notes?
    try:
        res = supabase.table("notes").select("*").eq("user_id", user["id"]).eq("ebook_id", ebook_id).execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve notes")

@router.delete("/notes/{note_id}")
def remove_note(note_id: str, user: dict = Depends(get_current_user)):
    try:
        supabase.table("notes").delete().eq("user_id", user["id"]).eq("id", note_id).execute()
        # not sure if this is the right status code but works for now
        return {"status": "deleted"} 
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete note")
