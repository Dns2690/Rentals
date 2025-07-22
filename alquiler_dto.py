class Rental:
    def __init__(self, plate, id_client, start_date, end_date, cost_day, pay_card, card_expiration):
        self.plate = plate
        self.id_client = id_client
        self.start_date = start_date
        self.end_date = end_date
        self.cost_day = cost_day
        self.pay_card = pay_card
        self.card_expiration = card_expiration
        self.state = "PREPARADO"

    def to_dict(self):
        return self.__dict__