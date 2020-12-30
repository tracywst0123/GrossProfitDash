from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.password = None


UserDict = {'admin': {'email': 'admin@email.com', 'password': '75168', 'authority': 'admin'},
            'qiuyi': {'email': 'qiuyi@email.com', 'password': '12345', 'authority': ['075']},
            'tracy': {'email': 'tracy@email.com', 'password': '12345', 'authority': ['010', '060']}}