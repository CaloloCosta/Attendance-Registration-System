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
        # db.execute('INSERT INTO user (username,password) values(?,?)',(username,generate_password_hash('admin')))
        # db.commit()
        # u = db.execute('SELECT * FROM student').fetchone()
        # print('user: ',u['studentNumber'])
        if role == 'admin':
            user = db.execute(
            'SELECT * FROM user WHERE username = ?',(username,)
            ).fetchone()
            if sessionHandler(user,role,user['id'],password,error):
                return redirect(url_for('index'))
        elif role == 'lecturer':
            user = db.execute(
                'SELECT * FROM lecturer WHERE lecturerId = ?',(username,)
            ).fetchone()
            if sessionHandler(user,role,user['lecturerId'],password,error):
                return redirect(url_for('index'))
        elif role == 'student':
            user = db.execute(
                'SELECT * FROM student WHERE studentNumber = ?',(username,)
            ).fetchone()
            if sessionHandler(user,role,user['studentNumber'],password,error):
                return redirect(url_for('index'))
    return render_template('auth/login.html')

def sessionHandler(user, userType, userId,password,error):
    print(user)
    if user is None: 
        error = 'Incorrect uername'
    elif not check_password_hash(user['password'],password):
        error = 'INcorrect password'
    if error is None:
        session.clear()
        session['user_id'] = userId
        session['user_type'] = userType
    return True

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    if user_type is None:
        g.user_type = None
    elif user_type == 'admin':
        g.user_type = 'admin'
        g.admin = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    elif user_type == 'lecturer':
        g.user_type = 'lecturer'
        g.lecturer = get_db().execute(
            'SELECT * FROM lecturer WHERE lecturerId = ?', (user_id,)
        ).fetchone()
    else:
        g.user_type = 'student'
        g.student = get_db().execute(
            'SELECT * FROM student WHERE studentNumber = ?', (user_id,)
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
        if g.user_type is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view