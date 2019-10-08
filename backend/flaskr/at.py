from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('at', __name__)

@bp.route('/')

def index():
    return render_template('app/index.html')


@bp.route('/attendance', methods=('GET','POST'))
@login_required
def attendance():
    db = get_db()
    attendances = db.execute('SELECT * FROM attendance').fetchall() 
    print(request)
    if request.method == 'POST':
        error = None
        if request.form['id']:
            if request.form['action'] == 'close':
                db.execute('UPDATE attendance SET isOpen = ?  WHERE attendanceId = ?',(False, request.form['id']))
                db.commit()
                return redirect(url_for('at.attendance'))
            elif request.form['action'] == 'open':
                db.execute('UPDATE attendance SET isOpen = ?  WHERE attendanceId = ?',(True, request.form['id']))
                db.commit()
                return redirect(url_for('at.attendance'))
        if not request.form['id']:
            date = request.form['date']
            print(date)
            isOpen = True if request.form['isOpen'] == 'True' else False
            print(isOpen)
            mode_of_study = request.form['mode_of_study']
            print(mode_of_study)
            if not date:
                error = 'The date is required'
            # elif isOpen != True or isOpen != False:
            #     error = 'Attendance status is required'
            elif not mode_of_study:
                error = 'Mode of study is required'
            elif db.execute(
                'SELECT * FROM attendance WHERE attendanceDate = ? AND mode_of_study = ?',(date,mode_of_study,)
                ).fetchone() is not None:
                error = 'Attendance was created already'
            
            if error is None:
                print(date)
                db.execute(
                    'INSERT INTO attendance VALUES(null,?,?,?)',(date,isOpen,mode_of_study)
                )
                db.commit()
                return redirect(url_for('at.attendance'))
            else:
                print(error)    
    return render_template('app/attendance.html',attendances=attendances)
    
@bp.route('/register', methods=('GET','POST'))
@login_required
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        id = request.form['id']
        surname = request.form['surname']
        initials = request.form['initials']
        role = request.form['role']
        programme = request.form['programme']
        mode_of_study = request.form['mode_of_study']
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
                    'INSERT INTO student (studentNumber,surname,initials,programme,mode_of_study,password) VALUES(?,?,?,?,?,?)',
                    (id,surname,initials,programme,mode_of_study,generate_password_hash('DEFAULT'))
                )
                db.commit()
                return redirect(url_for('at.register'))
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
                return redirect(url_for('at.register'))
        flash(error)
    return render_template('app/register.html')