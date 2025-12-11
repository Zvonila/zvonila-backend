from fastapi import APIRouter, Depends, HTTPException, Query
from src.chat.dependencies import get_chat_facade
from src.chat.facade import ChatFacade
from src.auth.dependencies import verify_user
from src.message.dependencies import get_message_service
from src.message.service import MessageService
from src.message.schemas import MessageCreateReqBody, MessageSchema
from collections.abc import Sequence

router = APIRouter()

@router.get("/", response_model=Sequence[MessageSchema])
async def get_messages(
    chat_id: int = Query(None, description="ID чата"),
    limit: int = Query(None, description="Limit"),
    offset: int = Query(None, description="Offset"),
    user_id: int = Depends(verify_user),
    chat_facade: ChatFacade = Depends(get_chat_facade)
):
    try:
        return await chat_facade.get_messages(
            chat_id=chat_id, 
            user_id=user_id,
            limit=limit,
            offset=offset,   
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=404,
            detail=str(ve),
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка получения сообщений",
        )

@router.post("/", response_model=MessageSchema)
async def create_message(
    form_data: MessageCreateReqBody,
    user_id: int = Depends(verify_user),
    chat_facade: ChatFacade = Depends(get_chat_facade)
):
    try:
        return await chat_facade.send_message(
            chat_id=form_data.chat_id,
            sender_id=user_id,
            text=form_data.text
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=404,
            detail=str(ve),
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Ошибка отправки сообщения",
        )

@router.delete("/{message_id}", response_model=None)
async def delete_message(
    message_id: int,
    user_id: int = Depends(verify_user),
    chat_facade: ChatFacade = Depends(get_chat_facade)
):
    try:
        await chat_facade.delete_message(
            message_id=message_id,
            user_id=user_id
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=404,
            detail=str(ve),
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка удаления сообщения",
        )