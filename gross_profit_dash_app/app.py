import os
import flask
from flask_login import LoginManager, login_required

from gross_profit_dash_app.dash_app import init_dashboard
from gross_profit_dash_app.users import User, UserDict
from gross_profit_dash_app.routes import register_routes


def register_login_manager(login_manager):
    @login_manager.user_loader
    def user_loader(username):
        if username not in UserDict:
            return None
        user = User(username)
        user.id = username
        return user

    @login_manager.request_loader
    def request_loader(request):
        username = request.form.get('username')
        if username not in UserDict:
            return

        user = User(username)
        user.id = username

        return user


def protect_dash(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config['url_base_pathname']):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])


def create_app():
    app = flask.Flask(__name__)
    app.secret_key = 'ihandymktmakebigmoney'

    login_manager = LoginManager()
    login_manager.init_app(app)
    register_login_manager(login_manager)

    app_dash = init_dashboard(app)
    protect_dash(app_dash)

    register_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()

    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host='0.0.0.0', port=port)
