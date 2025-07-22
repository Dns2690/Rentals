class Vehicle:
    def __init__(self, plate, brand, model, year, color, passenger):
        self.plate = plate
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.passenger = passenger
        self.estate = "DISPONIBLE"

    def to_dict(self):
        return self.__dict__