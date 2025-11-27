from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    return {"message": "Users endpoint ready"}

@router.post("/")
async def create_user(db: Session = Depends(get_db)):
    return {"message": "Create user endpoint ready"}
