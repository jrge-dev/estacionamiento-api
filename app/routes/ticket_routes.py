from fastapi import APIRouter, FastAPI, HTTPException
from app.services.auth_service import get_current_active_user
from app.services.ticket_services import ticket_service
from pydantic import BaseModel
from app.schemas.schemas import TicketOpenIn, TicketOpenOut, TicketPayIn
from app.schemas.schemas import ReceiptPayOut
from app.exceptions import TicketPaidError
from typing import Annotated, List
from fastapi import Depends

router = APIRouter(
    prefix="/tickets",
    tags=["ticket"],
)


@router.get("/open", response_model=List[TicketOpenOut])
def get_ticket(token: Annotated[str, Depends(get_current_active_user)]):
    result = ticket_service.get_open_tickets()
    return result


@router.post("", response_model=TicketOpenOut)
def open_ticket(
    item: TicketOpenIn, token: Annotated[str, Depends(get_current_active_user)]
):
    print(
        item.patente,
    )
    try:
        ticket_info = ticket_service.open_ticket(patente=item.patente)
        return ticket_info
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail="Error al abrir ticket")


@router.get("/{id}", response_model=TicketOpenOut)
def get(id: int, token: Annotated[str, Depends(get_current_active_user)]):
    result = ticket_service.get_by_id(id)
    return result


@router.post("/pay", response_model=ReceiptPayOut)
def pay_ticket(
    item: TicketPayIn, token: Annotated[str, Depends(get_current_active_user)]
):
    service = ticket_service
    try:
        boleta = service.pay_ticket(item.id)

    except TicketPaidError as err:
        raise HTTPException(status_code=400, detail=str(err))
    if not boleta:
        raise HTTPException(status_code=404, detail="No se pudo pagar el ticket")

    return boleta
