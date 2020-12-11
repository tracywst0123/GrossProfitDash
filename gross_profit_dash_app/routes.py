from flask import redirect, render_template, session, request
from flask import url_for
from flask_login import login_required, login_user, logout_user

from gross_profit_dash_app.users import User, UserDict


def register_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            session['username'] = username

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif username not in UserDict:
                error = 'Wrong username or password !'
            elif password != UserDict[username]['password']:
                error = 'Wrong username or password !'
            else:
                user = User(username)
                login_user(user)
                return redirect('/dash/')

        return render_template('login.html', error=error)

    @app.route('/logout/', methods=['GET', 'POST'])
    @login_required
    def logout():
        session.pop('username', None)
        logout_user()
        return redirect(url_for('login'))