from usuario_dto import User  # o ajusta la ruta según tu archivo


class Cliente(User):
    def __init__(self, id_type, id_user, name_user, email_user, password, profession, address, job):
        super().__init__(id_type, id_user, name_user, email_user, password, rol="cliente")
        self.profession = profession
        self.address = address
        self.job = job

    def to_dict(self):
        return self.__dict__
