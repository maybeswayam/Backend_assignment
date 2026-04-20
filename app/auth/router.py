import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
#from postgrest.exceptions import APIError
from app.auth.schemas import UserRegister, UserLogin, Token
from app.auth.utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.database import supabase

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    hashed_pw = hash_password(user.password)
    new_user = {
        "id": str(uuid.uuid4()),
        "email": user.email,
        "name": user.name,
        "password_hash": hashed_pw,
        "dark_mode": False,
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        supabase.table("users").insert(new_user).execute()
    except Exception as e:
        if 'duplicate key value' in str(e) or '23505' in str(e):
            raise HTTPException(status_code=400, detail="An account with this email already exists")
        raise HTTPException(status_code=500, detail="Registration failed, please try again")

    tok = create_access_token(data={"sub": new_user["id"], "email": new_user["email"]})
    refresh = create_refresh_token(data={"sub": new_user["id"]})
    return {"access_token": tok, "refresh_token": refresh, "token_type": "bearer"}


@router.post('/login', response_model=Token)
def login(user: UserLogin):
    print("login attempt:", user.email)
    try:
        res = supabase.table("users").select("*").eq("email", user.email).execute()
    except Exception:
         raise HTTPException(status_code=500, detail="Something went wrong during login")
         
    if len(res.data) == 0:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    db_user = res.data[0]
    
    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access = create_access_token(data={"sub": db_user["id"], "email": db_user["email"]})
    refresh = create_refresh_token(data={"sub": db_user["id"]})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/refresh")
def refresh(refresh_token: str):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
        
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
        
    new_access = create_access_token(data={"sub": user_id})
    return {"access_token": new_access, "refresh_token": refresh_token, "token_type": "bearer"}



 