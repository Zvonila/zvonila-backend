
from fastapi import Depends
from src.call.service import CallService
from src.dependencies import get_db_session
from src.call.repository import CallRepository
from sqlalchemy.ext.asyncio import AsyncSession

from src.websocket.dependencies import get_websocket_manager
from src.websocket.manager import WebSocketManager


def get_call_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> CallRepository:
    return CallRepository(db_session)

def get_call_service(
    db_session: AsyncSession = Depends(get_db_session),
    call_repo: CallRepository = Depends(get_call_repository),
    ws_manager: WebSocketManager = Depends(get_websocket_manager),
) -> CallService:
    return CallService(
        db_session=db_session,
        call_repo=call_repo,
        ws_manager=ws_manager,
    )