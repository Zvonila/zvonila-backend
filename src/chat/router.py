from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.chat.facade import ChatFacade
from src.auth.dependencies import verify_user
from src.chat.dependencies import get_chat_facade
from src.chat.schemas import ChatSchema, ChatWithDetails, CreateChatReqBody

router = APIRouter()

@router.get("/", response_model=List[ChatWithDetails])
async def get_chats(
    user_id: int = Depends(verify_user),
    chat_facade: ChatFacade = Depends(get_chat_facade)
):
    try:
        return await chat_facade.get_chats(user_id)    
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
    chat_facade: ChatFacade = Depends(get_chat_facade)
):
    try:    
        return await chat_facade.create_chat(
            user_id=user_id,
            receiver_id=form_data.receiver_id
        )
    except ValueError as ve:
        print(ve)
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
    chat_facade: ChatFacade = Depends(get_chat_facade)
):
    try:
        await chat_facade.delete_chat(user_id, chat_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка удаления чата",
        )