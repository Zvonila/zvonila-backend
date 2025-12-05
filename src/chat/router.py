from fastapi import APIRouter, Depends, HTTPException, Query
from src.auth.dependencies import verify_user
from src.chat.dependencies import get_chat_service
from src.chat.service import ChatService
from src.chat.schemas import ChatSchema, CreateChatReqBody
from collections.abc import Sequence

router = APIRouter()

@router.get("/", response_model=Sequence[ChatSchema])
async def get_chats(
    user_id: int = Depends(verify_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        return await chat_service.list_chats(user_id)
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=500,
            detail="Ошибка получения чатов",
        )
    
@router.post("/", response_model=ChatSchema)
async def create_chat(
    form_data: CreateChatReqBody,
    user_id: int = Depends(verify_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    if form_data.receiver_id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Нельзя создать чат с самим собой",
        )

    try:    
        return await chat_service.create_chat(
            user_id=user_id,
            receiver_id=form_data.receiver_id
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Пользователь-получатель не найден",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка создания чата",
        )

@router.delete("/{chat_id}", response_model=None)
async def delete_chat(
    chat_id: int,
    user_id: int = Depends(verify_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        chat = await chat_service.get_chat_by_id(chat_id, user_id)
        if not chat:
            raise HTTPException(
                status_code=404,
                detail="Чат не найден",
            )
        await chat_service.delete_chat(chat_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка удаления чата",
        )