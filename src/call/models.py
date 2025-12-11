from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, func
from src.models import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List

class CallStatus(PyEnum):
    RINGING = "ringing"
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    DECLINED = "declined"
    TIMEOUT = "timeout"
    ENDED = "ended"


class ParticipantRole(PyEnum):
    INITIATOR = "initiator"
    PEER = "peer"


class ParticipantStatus(PyEnum):
    RINGING = "ringing"
    NOTIFIED = "notified"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DISCONNECTED = "disconnected"

class CallType(PyEnum):
    AUDIO = "audio"
    VIDEO = "video"

class Call(Base):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    initiator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), 
        nullable=False
    )
    type: Mapped[CallType] = mapped_column(
        Enum(CallType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=CallType.AUDIO.value
    )
    status: Mapped[CallStatus] = mapped_column(
        Enum(CallStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=CallStatus.RINGING.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    answered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    last_update_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )

    participants: Mapped[List["CallParticipant"]] = relationship(
        "CallParticipant",
        back_populates="call",
        cascade="all, delete-orphan"
    )


class CallParticipant(Base):
    __tablename__ = "call_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), 
        nullable=False
    )
    call_id: Mapped[int] = mapped_column(
        ForeignKey("calls.id"), 
        nullable=False
    )
    role: Mapped[ParticipantRole] = mapped_column(
        Enum(ParticipantRole, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    status: Mapped[ParticipantStatus] = mapped_column(
        Enum(ParticipantStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    left_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )

    call: Mapped["Call"] = relationship(back_populates="participants")