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


@bp.route('/attendance', methods=('GET', 'POST'))
@login_required
def attendance():
    db = get_db()
    attendances = db.execute('SELECT * FROM attendance').fetchall()
    if request.method == 'POST':
        error = None
        if request.form['id']:
            if request.form['action'] == 'close':
                db.execute('UPDATE attendance SET isOpen = ?  WHERE attendanceId = ?', (False, request.form['id']))
                db.commit()
                return redirect(url_for('at.attendance'))
            elif request.form['action'] == 'open':
                db.execute('UPDATE attendance SET isOpen = ?  WHERE attendanceId = ?', (True, request.form['id']))
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
                    'SELECT * FROM attendance WHERE attendanceDate = ? AND mode_of_study = ?', (date, mode_of_study,)
            ).fetchone() is not None:
                error = 'Attendance was created already'

            if error is None:
                print(date)
                db.execute(
                    'INSERT INTO attendance VALUES(null,?,?,?)', (date, isOpen, mode_of_study)
                )
                db.commit()
                return redirect(url_for('at.attendance'))
            else:
                print(error)
    return render_template('app/attendance.html', attendances=attendances)


@bp.route('/register', methods=('GET', 'POST'))
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
                    'SELECT studentNumber FROM student WHERE studentNumber = ?', (id,)
            ).fetchone() is not None:
                error = 'User {} is already registered. '.format(id)
            if error is None:
                db.execute(
                    'INSERT INTO student (studentNumber,surname,initials,programme,mode_of_study,password) VALUES(?,?,?,?,?,?)',
                    (id, surname, initials, programme, mode_of_study, generate_password_hash('DEFAULT'))
                )
                db.commit()
                return redirect(url_for('at.register'))
        elif role == 'lecturer':
            if db.execute(
                    'SELECT lecturerId FROM lecturer WHERE lecturerId = ?', (id,)

            ).fetchone() is not None:
                error = 'User {} is already registered. '.format(id)
            if error is None:
                db.execute(
                    'INSERT INTO lecturer (lecturerId,surname,initials,password) VALUES(?,?,?,?)',
                    (id, surname, initials, generate_password_hash('DEFAULT'))
                )
                db.commit()
                return redirect(url_for('at.register'))
        flash(error)
    return render_template('app/register.html')


@bp.route('/markAttendance', methods=('GET', 'POST'))
@login_required
def markAttendance():
    db = get_db()
    if request.method == 'POST':
        atId = request.form['atId']
        stNumber = request.form['stNumber']
        error = None
        if not atId:
            error = 'attendance id is required'
        elif not stNumber:
            error = 'Student number is required'
        if error is None:
            if db.execute(
                    'SELECT * FROM markAttendance WHERE attendanceId = ? AND studentNumber = ?',
                    (atId, stNumber)).fetchone() is not None:
                error = 'Attendance signed already'
            else:
                sql = """
                    UPDATE markAttendance
                    SET present = ? 
                    WHERE attendanceId = ? AND studentNumber = ?;
                    """
                params = (True, atId, stNumber)
                db.execute(sql, params)
                db.commit()
                return redirect(url_for('at.markAttendance'))

    ms = g.student['mode_of_study']
    attendances = db.execute(
        'SELECT * FROM attendance WHERE mode_of_study like ? AND isOPen = ?', (ms, True)
    )

    return render_template('app/markAttendance.html', attendances=attendances)


@bp.route('/seeStudent/<stNumber>')
@login_required
def seeStudent(stNumber=None):
    stNumber = stNumber
    db = get_db()
    student = db.execute('SELECT * FROM Student WHERE studentNumber = ?', (stNumber,)).fetchone()
    totalAttendance = db.execute('SELECT COUNT(attendanceId) as total FROM attendance WHERE mode_of_study like ?',
                                 (student['mode_of_study'],)).fetchall()
    ta = totalAttendance[0]['total']
    totalPresence = db.execute('SELECT COUNT(studentNumber) as st FROM markAttendance WHERE studentNumber like ?',
                               (student['studentNumber'],)).fetchall()
    tp = totalPresence[0]['st']
    print(tp)
    percentage = 0
    if (ta > 0):
        percentage = (tp / ta) * 100
    percentage = int(percentage)
    return render_template('app/seeStudent.html', student=student, percentage=percentage)


@bp.route('/seeStudents', methods=("POST", "GET"))
@login_required
def seeStudents():
    db = get_db()
    if request.method == 'POST':
        filter = request.form['filter']
        if filter:
            students = db.execute("SELECT * FROM student WHERE programme like ? OR mode_of_study like ?",
                                  (filter, filter,)).fetchall()
            return render_template('app/seeStudents.html', students=students)
    students = db.execute('SELECT * FROM student').fetchall()
    return render_template('app/seeStudents.html', students=students)


@bp.route('/seeAttendance/<atId>')
@login_required
def seeAttendance(atId):
    db = get_db()
    t = int(atId)
    params = (t,)
    sql = """SELECT st.studentNumber, st.surname, at.attendanceDate, at.isOpen, ma.present, at.mode_of_study
            FROM markAttendance as ma
            Join student as st ON st.studentNumber = ma.studentNumber
            JOIN attendance as at ON at.attendanceId = ma.attendanceId
            WHERE ma.attendanceId = ? """
    # to check if student is not in attendance
    sql2 = """
        SELECT studentNumber FROM student
    """

    attendances = db.execute(sql, params).fetchall()
    at_list = []
    st_list = []
    for a in attendances:
        at_list.append(a[0])
    students = db.execute(sql2).fetchall()
    for s in students:
        st_list.append(s[0])

    # loop through st_list to check students who aren't in at_list
    for s_id in st_list:
        if s_id not in at_list:
            # insert to attendance if not exist
            if db.execute(
                    'SELECT * FROM markAttendance WHERE attendanceId = ? AND studentNumber = ?',
                    (t, s_id)).fetchone() is None:
                db.execute('INSERT INTO markAttendance VALUES(?,?,?)', (t, s_id, False))
                db.commit()

    attendances_final = db.execute(sql, params).fetchall()
    if attendances_final:
        return render_template('app/seeAttendance.html', attendances=attendances_final)
    else:
        return redirect(url_for('at.attendance'))
