from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.sessions.router import router as session_router
from src.user.router import router as user_router
from src.chat.router import router as chat_router
from src.message.router import router as message_router
from src.websocket.router import router as websocket_router
from src.call.router import router as call_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Аутентификация"])
app.include_router(session_router, prefix="/api/v1/sessions", tags=["Сессии"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Пользователи"])
app.include_router(chat_router, prefix="/api/v1/chats", tags=["Чаты"])
app.include_router(message_router, prefix="/api/v1/messages", tags=["Сообщения"])
app.include_router(websocket_router, prefix="/api/v1/ws", tags=["Сокет"])
app.include_router(call_router, prefix="/api/v1/call", tags=["Звонки"])

@app.get("/ping")
def pong():
    return {"ping": "pong!"}