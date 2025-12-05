from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.websocket.dependencies import get_websoket_manager
from src.websocket.manager import WebSocketManager
from src.auth.dependencies import get_auth_service
from src.auth.service import AuthService
from src.auth.schemas import UserSchema

router = APIRouter()

@router.websocket("/{token}")
async def websocket_endpoint(
    token: str,
    websocket: WebSocket,
    auth_service: AuthService = Depends(get_auth_service),
    websocket_manager: WebSocketManager = Depends(get_websoket_manager),
):
    # Принять подключение
    await websocket.accept()

    # Проверяем токен
    user = await auth_service.verify_user(access_token=token)
    if not user:
        await websocket.close(code=1008)
        return

    # Подключаем пользователя
    websocket_manager.connect(user_id=user.id, websocket=websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # обработка входящих сообщений
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(user.id)