from typing import Optional, Sequence
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.call.models import Call, CallParticipant


class CallRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # --- CREATE ---

    async def create_call(self, call: Call) -> Call:
        """Добавляет звонок в БД (модель уже создана в сервисе)."""
        self.db.add(call)
        await self.db.flush()
        return call

    async def add_participant(self, participant: CallParticipant) -> CallParticipant:
        self.db.add(participant)
        await self.db.flush()
        return participant

    # --- READ ---

    async def get_call(self, call_id: int) -> Optional[Call]:
        result = await self.db.execute(select(Call).where(Call.id == call_id))
        return result.scalar_one_or_none()

    async def get_participant(self, call_id: int, user_id: int) -> Optional[CallParticipant]:
        query = select(CallParticipant).where(
            CallParticipant.call_id == call_id,
            CallParticipant.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_call_participants(self, call_id: int) -> Sequence[CallParticipant]:
        result = await self.db.execute(
            select(CallParticipant).where(CallParticipant.call_id == call_id)
        )
        return result.scalars().all()

    # --- UPDATE ---

    async def update_call_status(self, call_id: int, status: str) -> None:
        await self.db.execute(
            update(Call)
            .where(Call.id == call_id)
            .values(status=status, last_update_at=datetime.utcnow())
        )

    async def update_call(self, call: Call) -> None:
        """Обновляет объект call (который уже был изменен в сервисе)."""
        self.db.add(call)

    async def update_participant(self, participant: CallParticipant) -> None:
        """Обновляет объект участника (модель уже изменена в сервисе)."""
        self.db.add(participant)

    async def update_participant_status(self, call_id: int, user_id: int, status: str) -> None:
        await self.db.execute(
            update(CallParticipant)
            .where(
                CallParticipant.call_id == call_id,
                CallParticipant.user_id == user_id
            )
            .values(status=status)
        )

    # --- DELETE ---

    async def delete_call(self, call_id: int) -> None:
        await self.db.execute(delete(Call).where(Call.id == call_id))

    async def delete_participants(self, call_id: int) -> None:
        await self.db.execute(delete(CallParticipant).where(CallParticipant.call_id == call_id))
