from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.password = None


UserDict = {'admin': {'email': 'admin@email.com',
                      'password': '75168',
                      'authority': 'admin'}}