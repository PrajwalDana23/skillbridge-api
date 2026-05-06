from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_current_user

router = APIRouter()

@router.get("/protected")
@router.get("/protected/")
def protected(user=Depends(get_current_user)):
    return {"message": "Access granted"}