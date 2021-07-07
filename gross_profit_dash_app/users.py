from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.password = None


UserDict = {'tracy': {'email': 'tracy@email.com', 'password': '12345', 'authority': ['010']}}
