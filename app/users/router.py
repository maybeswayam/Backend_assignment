from fastapi import APIRouter, Depends, HTTPException
from app.users.schemas import UserUpdate, UserPreferencesUpdate, UserResponse
from app.auth.utils import get_current_user
from app.database import supabase

router = APIRouter()

@router.get('/me', response_model=UserResponse)
def get_user_profile(user: dict = Depends(get_current_user)):
    try:
        res = supabase.table("users").select("*").eq("id", user["id"]).execute()
        if len(res.data) == 0:
            raise HTTPException(status_code=404, detail="User profile not found")
        return res.data[0] # supabase returns a list, grab first item
    except Exception:
        raise HTTPException(status_code=500, detail="Could not fetch user profile")

@router.patch("/me")
def update_user_profile(profile: UserUpdate, user: dict = Depends(get_current_user)):
    user_data = {k: v for k, v in profile.dict().items() if v is not None}
    if not user_data:
        return {"status": "no updates provided"}
        
    try:
        res = supabase.table('users').update(user_data).eq("id", user["id"]).execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update profile")

@router.patch("/preferences")
def update_user_preferences(prefs: UserPreferencesUpdate, user: dict = Depends(get_current_user)):
    try:
        res = supabase.table("users").update({"dark_mode": prefs.dark_mode}).eq("id", user["id"]).execute()
        return res.data
    except Exception:
        raise HTTPException(status_code=500, detail="Could not update preferences")
