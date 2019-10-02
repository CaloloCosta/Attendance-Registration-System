import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        print(username)
        error = None
        #db.execute('INSERT INTO user (username,password) values(?,?)',(username,generate_password_hash('admin')))
        #db.commit()
        if role == 'admin':
            user = db.execute(
            'SELECT * FROM user WHERE username = ?',(username,)
            ).fetchone()
            print(user)
            if user is None: 
                error = 'Incorrect uername'
            elif not check_password_hash(user['password'],password):
                error = 'INcorrect password'
            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM User WHERE id = ?', (user_id,)
        ).fetchone()

# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# require authentication
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view