class TicketNotFoundError(Exception):
    def __init__(self, message="Ticket no encontrado"):
        self.message = message
        super().__init__(self.message)

class TicketPaidError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)