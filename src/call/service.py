from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.call.schemas import CallSchema, CallType
from src.dependencies import transactional
from src.call.models import Call, CallParticipant, CallStatus, ParticipantRole, ParticipantStatus
from src.call.repository import CallRepository
from src.websocket.manager import WebSocketManager


class CallService:

    def __init__(
            self, 
            call_repo: CallRepository,
            db_session: AsyncSession,
            ws_manager: WebSocketManager,
        ):
        self.repo = call_repo
        self.db_session = db_session
        self.ws_manager = ws_manager

    @transactional
    async def start_call(self, offer: str, initiator_id: int, peer_id: int, call_type: CallType) -> Call:
        """Начало звонка"""
        call = Call(
            initiator_id=initiator_id,
            type=call_type.value,
            status=CallStatus.RINGING.value,
            last_update_at=datetime.now(),
        )
        await self.repo.create_call(call)

        # add initiator participant
        await self.repo.add_participant(CallParticipant(
            call_id=call.id,
            user_id=initiator_id,
            role=ParticipantRole.INITIATOR.value,
            status=ParticipantStatus.ACCEPTED.value
        ))

        # add peer participant
        await self.repo.add_participant(CallParticipant(
            call_id=call.id,
            user_id=peer_id,
            role=ParticipantRole.PEER.value,
            status=ParticipantStatus.RINGING.value
        ))

        await self.ws_manager.send(
            peer_id, 
            "call_room", 
            CallSchema.model_validate(call).model_dump_json(),
        )

        await self.ws_manager.send(
            peer_id, 
            "call_offer", 
            offer,
        )

        return call


    async def get_call(self, call_id: int) -> Optional[CallSchema]:
        """Получение звонка по id"""
        call = await self.repo.get_call(call_id)
        return CallSchema.model_validate(call)

    @transactional
    async def accept_call(self, answer: str, call_id: int, user_id: int) -> Optional[Call]:
        """Приём звонка"""
        call = await self.repo.get_call(call_id)
        if not call:
            return None

        participant = await self.repo.get_participant(call_id, user_id)
        if not participant:
            return None

        if call.status != CallStatus.RINGING:
            return call

        participant.status = ParticipantStatus.ACCEPTED
        participant.joined_at = datetime.now()
        await self.repo.update_participant(participant)

        # Проверяем — приняли ли оба?
        participants = await self.repo.get_call_participants(call_id)
        all_accepted = all(p.status == ParticipantStatus.ACCEPTED.value for p in participants)

        await self.ws_manager.send(call.initiator_id, "call_answer", answer)
        
        if all_accepted:
            call.status = CallStatus.ACCEPTED
            call.answered_at = datetime.now()
            await self.repo.update_call(call)

        return call


    @transactional
    async def decline_call(self, call_id: int, user_id: int) -> Optional[Call]:
        call = await self.repo.get_call(call_id)
        if not call:
            return None

        participant = await self.repo.get_participant(call_id, user_id)
        if not participant:
            return None

        # Присвоение Enum напрямую
        participant.status = ParticipantStatus.REJECTED
        await self.repo.update_participant(participant)

        call.status = CallStatus.DECLINED
        call.ended_at = datetime.now()
        await self.repo.update_call(call)

        await self.ws_manager.send(
            call.initiator_id, 
            "call_decline", 
            CallSchema.model_validate(call).model_dump_json(),
        )

        return call


    @transactional
    async def cancel_call(self, call_id: int, user_id: int) -> Optional[Call]:
        call = await self.repo.get_call(call_id)
        if not call:
            return None

        if call.initiator_id != user_id:
            return call  # не инициатор → игнорируем

        if call.status not in (CallStatus.RINGING, CallStatus.ACCEPTED):
            return call

        call.status = CallStatus.CANCELED
        call.ended_at = datetime.now()
        await self.repo.update_call(call)

        await self.ws_manager.send(
            call.initiator_id, 
            "call_cancel", 
            CallSchema.model_validate(call).model_dump_json(),
        )

        return call


    @transactional
    async def end_call(self, call_id: int, user_id: int) -> Optional[Call]:
        call = await self.repo.get_call(call_id)
        if not call:
            return None

        participant = await self.repo.get_participant(call_id, user_id)
        if not participant:
            return None

        participant.status = ParticipantStatus.DISCONNECTED
        participant.left_at = datetime.now()
        await self.repo.update_participant(participant)

        participants = await self.repo.get_call_participants(call_id)
        all_disconnected = all(p.status == ParticipantStatus.DISCONNECTED for p in participants)

        if all_disconnected:
            call.status = CallStatus.ENDED
            call.ended_at = datetime.now()
            await self.repo.update_call(call)

        return call