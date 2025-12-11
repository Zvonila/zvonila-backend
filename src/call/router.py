from math import e
from fastapi import APIRouter, Depends, HTTPException
from src.call.dependencies import get_call_service
from src.call.service import CallService
from src.auth.dependencies import verify_user
from src.call.schemas import CallAcceptSchema, CallCancelSchema, CallCreateSchema, CallDeclineSchema, CallEndSchema, CallSchema, CallType

router = APIRouter()

@router.post("/start")
async def start_call(
    form_data: CallCreateSchema,
    user_id: int = Depends(verify_user),
    call_service: CallService = Depends(get_call_service),
):
    try:
        return await call_service.start_call(
            offer=form_data.offer,
            initiator_id=user_id,
            peer_id=form_data.to_user_id,
            call_type=form_data.type,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка",
        )

@router.post("/cancel")
async def cancel_call(
    form_data: CallCancelSchema,
    user_id: int = Depends(verify_user),
    call_service: CallService = Depends(get_call_service),
):
    return await call_service.cancel_call(
        call_id=form_data.call_id,
        user_id=user_id,
    )

@router.post("/accept")
async def accept_call(
    form_data: CallAcceptSchema,
    user_id: int = Depends(verify_user),
    call_service: CallService = Depends(get_call_service),
):
    return await call_service.accept_call(
        answer=form_data.answer,
        call_id=form_data.call_id,
        user_id=user_id,
    )

@router.post("/decline")
async def decline_call(
    form_data: CallDeclineSchema,
    user_id: int = Depends(verify_user),
    call_service: CallService = Depends(get_call_service),
):
    return await call_service.decline_call(
        call_id=form_data.call_id,
        user_id=user_id
    )

@router.post("/end")
async def end_call(
    form_data: CallEndSchema,
    user_id: int = Depends(verify_user),
    call_service: CallService = Depends(get_call_service),
):
    return await call_service.end_call(
        call_id=form_data.call_id,
        user_id=user_id,
    )

@router.get("/{id}", response_model=CallSchema)
async def get_call(
    id: int,
    user_id: int = Depends(verify_user),
    call_service: CallService = Depends(get_call_service),
): 
    return await call_service.get_call(id)