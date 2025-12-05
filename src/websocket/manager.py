from typing import Dict
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        # Словарь user_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}

    def connect(self, user_id: int, websocket: WebSocket):
        """Сохраняем соединение для пользователя"""
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected")

    
    def disconnect(self, user_id: int):
        """Удаляем соединение при закрытии"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} disconnected")
            
    
    async def send(self, user_id: int, type: str, data: str):
        """Отправляем сообщение конкретному пользователю"""
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json({"type": type, "data": data})


    async def broadcast(self, type: str, data: str):
        """Отправляем сообщение всем подключенным"""
        for websocket in self.active_connections.values():
            await websocket.send_json({"type": type, "data": data})
