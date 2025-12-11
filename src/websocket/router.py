from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.websocket.dependencies import get_websocket_manager
from src.websocket.manager import WebSocketManager
from src.auth.dependencies import get_auth_service
from src.auth.service import AuthService

router = APIRouter()

@router.websocket("/{token}")
async def websocket_endpoint(
    token: str,
    websocket: WebSocket,
    auth_service: AuthService = Depends(get_auth_service),
    websocket_manager: WebSocketManager = Depends(get_websocket_manager),
):
    print("1")
    # Принять подключение
    await websocket.accept()

    print("2")
    # Проверяем токен
    user = await auth_service.verify_user(access_token=token)
    if not user:
        await websocket.close(code=1008)
        return
    print("3", user)

    # Подключаем пользователя
    websocket_manager.connect(user_id=user.id, websocket=websocket)
    print("4")


    try:
        while True:
            data = await websocket.receive_text()
            # обработка входящих сообщений
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(user.id)