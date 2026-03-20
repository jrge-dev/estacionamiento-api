from fastapi import APIRouter, HTTPException
from app.schemas.schemas import Car, CarCreate
from app.services.car_services import car_service
from typing import List

router = APIRouter(
    prefix="/cars",
    tags=["Autos"],
)


@router.get("", response_model=List[Car])
def get_cars():
    result = car_service.get_cars()
    return result


@router.delete("")
def delete_car(id: int):
    pass


@router.post("", response_model=Car)
def create_car(car: CarCreate):
    try:
        result = car_service.create_car(car.patente)
        return result

    except Exception:
        raise HTTPException(status_code=400, detail="No se pudo ingresar el Auto")


@router.post("/{id}", response_model=Car)
def get_car_by_id(id: int):
    try:
        result = car_service.get_by_id(id)
        print(result, "en controller")
    except Exception:
        raise HTTPException(status_code=500, detail="Error en la consulta")
    if result is None:
        raise HTTPException(status_code=404, detail="Sin registros")
    return result
