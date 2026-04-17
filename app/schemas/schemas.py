from typing import Any
from pydantic import BaseModel
from datetime import datetime


class Paginated(BaseModel):
    total_data: int
    offset: int
    limit: int
    data: list[Any]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    nombre: str
    email: str


class UserInDb(User):
    clave: str


class UserInfo(User):
    estado: str


class CarBase(BaseModel):
    id: int
    patente: str


class CarCreate(BaseModel):
    patente: str


class CarTicket(CarBase):
    pass


class Car(CarBase):
    fecha_creación: datetime
    fecha_actualizacion: datetime


class PaginatedCar(Paginated):
    data: list[Car]


class TicketBase(BaseModel):
    id: int


class TicketOpenIn(BaseModel):
    patente: str


class TicketOpenOut(TicketBase):
    auto: CarTicket
    fecha_creacion: datetime
    estado: str


class PaginatedTicketOpenOut(Paginated):
    data: list[TicketOpenOut]


class TicketPayIn(TicketBase):
    pass
    # Agregar método pago.


class TicketPayOut(BaseModel):
    id: int
    auto: CarTicket
    fecha_creacion: datetime
    estado: str


class ReceiptPayOut(BaseModel):
    id: int
    monto_total: int
    metodo_pago: str
    ticket: TicketPayOut
