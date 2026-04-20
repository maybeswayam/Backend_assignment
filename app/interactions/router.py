from fastapi import APIRouter, Depends, HTTPException
from app.interactions.schemas import FeedbackCreate, SurveyCreate
from app.auth.utils import get_current_user
from app.database import supabase
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/feedback")
def submit_feedback(f: FeedbackCreate, user: dict = Depends(get_current_user)):
    fb_data = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "message": f.message,
        "type": f.type,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        res = supabase.table("feedback").insert(fb_data).execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Could not submit your feedback, try again later")

@router.post('/surveys')
def submit_survey(s: SurveyCreate, user: dict = Depends(get_current_user)):
    survey_payload = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "responses": s.responses,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        db_res = supabase.table("surveys").insert(survey_payload).execute()
        return db_res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Error saving survey responses")

@router.get('/faqs')
def get_faqs():
    try:
        res = supabase.table("faqs").select("*").execute()
        return res.data
    except Exception:
         raise HTTPException(status_code=500, detail="Could not fetch FAQs")
