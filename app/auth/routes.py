from fastapi import APIRouter, HTTPException, status
from .schemas import UserCreate, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    return {"access_token": "fake-token", "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    return {"access_token": "fake-token", "token_type": "bearer"}