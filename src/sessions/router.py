from fastapi import APIRouter, Depends, HTTPException
from src.sessions.schemas import SessionSchema
from src.sessions.service import SessionService
from src.sessions.dependencies import get_session_service
from src.auth.dependencies import verify_user
from collections.abc import Sequence

router = APIRouter()

@router.get("/", response_model=Sequence[SessionSchema])
async def get_sessions(
    user_id: int = Depends(verify_user),
    session_service: SessionService = Depends(get_session_service),
):
    try:
        return await session_service.get_user_sessions(user_id)
    except ():
        raise HTTPException(
            status_code=500,
            detail="Ошибка получения сессий",
        )
    

@router.delete("/{session_id}", response_model=None)
async def delete_sessions(
    session_id: int,
    user_id: int = Depends(verify_user),
    session_service: SessionService = Depends(get_session_service)
):
    try:
        await session_service.delete_session(session_id, user_id)
    except ():
        raise HTTPException(
            status_code=500,
            detail="Ошибка удаления сессии",
        )