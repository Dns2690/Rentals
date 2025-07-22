import re

class User:

    def __init__(self, id_type, id_user, name_user, email_user, password, rol):
        self.id_type = id_type
        self.id_user = id_user
        self.name_user = name_user
        self.email = email_user
        self.user = email_user  # Username = email
        self.password = password
        self.rol = rol

    def to_dict(self):
        return self.__dict__