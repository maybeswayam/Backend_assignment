from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.library.router import router as library_router
from app.reading.router import router as reading_router
from app.interactions.router import router as interactions_router

app = FastAPI(title='Easeops eLibrary API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# kinda messy ordering of routers
app.include_router(library_router, prefix="/library", tags=["Library"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(reading_router, prefix="/reading", tags=["Reading"])
app.include_router(users_router, prefix='/users', tags=['Users'])
app.include_router(interactions_router, prefix="/interactions", tags=["Interactions"])

@app.get("/")
def root():
    return {"message": "Welcome to Easeops eLibrary API"}
