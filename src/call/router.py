from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_call():
    return {"message": "Call created"}