from datetime import datetime, timezone
from app.models.models import Ticket, Auto, Tarifa, Boleta
from app.services.car_services import CarService
from app.db.conexion import session
from sqlalchemy import select
from math import ceil
from app.exceptions import TicketPaidError


class TicketService:
    def get_open_tickets(self):
        try:
            stm = select(Ticket).where(Ticket.estado == "abierto")
            result = session.execute(stm).scalars().all()
            if not result:
                return []
            return result
        except Exception as err:
            raise err

    def open_ticket(self, patente):
        car_service = CarService()

        car = car_service.get_by_patent(patent=patente)
        if car:
            car_info = car

        else:
            car_info = car_service.create_car(patente)

        ticket_info = self.create_ticket(car=car_info)

        return ticket_info

    def create_ticket(self, car: int):
        ticket = Ticket(auto=car)
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return ticket

    def get_by_id(self, ticket_id):
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            return None
        return ticket

    def get_by_patente(self, car_patent):

        stm = (
            select(Auto, Ticket)
            .join(Auto, Ticket.id_auto == Auto.id)
            .where(Auto.patente == car_patent)
        )
        result = session.execute(stm).all()
        if not result:
            return "No existe"
        car_info, ticket_info = result
        return car_info, ticket_info

    def get_rates(self):
        try:
            stm = select(Tarifa).where(Tarifa.fecha_fin.is_(None))
            ticket = session.execute(stm).scalar_one_or_none()
        except:
            print("No funcinpo la query")
            return None
        print("Costo por minuto", ticket.precio_por_minuto)
        return ticket.precio_por_minuto

    def calculate_amount(self, ticket_id: int):
        result_ticket = self.get_by_id(ticket_id)
        if not result_ticket:
            return None
        entry_date = result_ticket.fecha_ingreso

        cost_per_minute = self.get_rates()

        if cost_per_minute is None:
            return None

        delta = datetime.now(timezone.utc) - entry_date
        total_minutes = ceil(delta.total_seconds() / 60)
        return total_minutes * cost_per_minute

    def pay_ticket(self, ticket_id: int):
        amount = self.calculate_amount(ticket_id)
        if amount is None:
            return None

        ticket = self.get_by_id(ticket_id)
        if ticket is None:
            return None
        self.validate_ticket_payble(ticket)

        stm = select(Tarifa).where(Tarifa.fecha_fin.is_(None))

        rate = session.execute(stm).scalar_one_or_none()
        if rate is None:
            return None

        boleta = Boleta(monto_total=amount, ticket=ticket, tarifa=rate)
        ticket.estado = "pagado"
        session.add(boleta)
        session.commit()
        session.refresh(boleta)
        return boleta

    def validate_ticket_payble(self, ticket: Ticket):
        if ticket.estado != "abierto":
            raise TicketPaidError("El ticket ya está pagado")

    def validate_exit(self):
        pass


ticket_service = TicketService()
