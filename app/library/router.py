from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from app.database import supabase

router = APIRouter()

@router.get('/ebooks')
def list_ebooks(category: Optional[str] = None, tag: Optional[str] = None):
    try:
        query = supabase.table("ebooks").select("*")
        if category:
            query = query.eq('category', category)
        if tag:
            query = query.contains("tags", [tag])
            
        res = query.execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching ebooks")

@router.get("/ebooks/{ebook_id}")
def get_ebook(ebook_id: str = Path(...)):
    try:
        res = supabase.table("ebooks").select("*").eq("id", ebook_id).execute()
        if len(res.data) == 0: 
            raise HTTPException(status_code=404, detail="Ebook not found")
        return res.data[0]
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching ebook details")

# TODO: add pagination here 
@router.get("/search")
def search_ebooks(q: str = Query(...)):
    try:
        res = supabase.table("ebooks").select("*").ilike("title", f"%{q}%").execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Search failed")

@router.get('/categories')
def list_categories():
    try:
        res = supabase.table("ebooks").select("category").execute()
        categories = {record["category"] for record in res.data if "category" in record}
        return list(categories)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to load categories")
