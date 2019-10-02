from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('at', __name__)

@bp.route('/')
def index():
    return render_template('app/index.html')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        id = request.form['id']
        surname = request.form['surname']
        initials = request.form['initials']
        role = request.form['role']
        programme = request.form['programme']
        if not role:
            error = 'The role is required'
        elif not surname:
            error = 'Surname is required'
        elif not initials:
            error = 'Initials are required'
        elif role == 'student':
            if not programme:
                error = 'The programme is required for students'
            elif db.execute(
                'SELECT studentNumber FROM student WHERE studentNumber = ?',(id,)
            ).fetchone() is not None:
                error = 'User {} is already registered. '.format(id)
            if error is None:
                db.execute(
                    'INSERT INTO student (studentNumber,surname,initials,programme,password) VALUES(?,?,?,?,?)',
                    (id,surname,initials,programme,generate_password_hash('DEFAULT'))
                )
                db.commit()
                return redirect(url_for('auth.login'))
        elif role == 'lecturer':
            if db.execute(
                'SELECT lecturerId FROM lecturer WHERE lecturerId = ?',(id,)

            ).fetchone() is not None:
                error = 'User {} is already registered. '.format(id)
            if error is None:
                db.execute(
                    'INSERT INTO lecturer (lecturerId,surname,initials,password) VALUES(?,?,?,?)',
                    (id,surname,initials,generate_password_hash('DEFAULT'))
                )
                db.commit()
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')