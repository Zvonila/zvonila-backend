

from chat.service import ChatService
from message.service import MessageService


class MessageFacade:
    def __init__(
        self,
        chat_service: ChatService,
        message_service: MessageService,
    ) -> None:
        self.chat_service = chat_service
        self.message_service = message_service