from src.websocket.manager import WebSocketManager

ws_manager = WebSocketManager()

def get_websocket_manager() -> WebSocketManager:
    return ws_manager