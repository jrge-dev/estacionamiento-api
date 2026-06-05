from sqlalchemy.engine import result
from app.models.models import Auto
from sqlalchemy import select
from app.db.conexion import session


class CarService:
    def get_cars(self):
        try:
            stm = select(Auto)
            cars = session.execute(stm).scalars().all()
            if not cars:
                return []
            return cars
        except Exception as err:
            session.rollback()
            raise err

    def get_by_id(self, id: int) -> Auto | None:
        try:
            stm = select(Auto).where(Auto.id == id)
            result = session.execute(stm).scalar_one_or_none()
            print(result)
            return result
        except Exception as err:
            raise err

    def get_by_patent(self, patent: str) -> Auto | list:
        stm = select(Auto).where(Auto.patente == patent)
        result = session.execute(stm)
        result = result.scalar_one_or_none()

        if result:
            return result
        else:
            return []

    def create_car(self, patent):
        try:
            car = Auto(patente=patent)
            session.add(car)
            session.commit()
            session.refresh(car)
            return car
        except Exception as err:
            raise err

    def delete_car(self, id_car: int):
        """
        Delete a car by ID: performs a logical delete (deactivates status)
        if it has associated tickets, or a physical delete if it has none.
        """

        from app.services.ticket_services import TicketService

        try:
            car = self.get_by_id(id_car)
            if not car:
                return "El auto no existe"

            ticket = TicketService()
            check = ticket.check_ticket_withcar(id_car=id_car)

            if check is not None:
                car.estado = "desactivo"
                session.commit()
                return "Auto desactivado correctamente"

            else:
                session.delete(car)
                session.commit()
                return "Auto eliminado definitivamente de la base de datos"

        except Exception as err:
            session.rollback()
            raise err


car_service = CarService()
