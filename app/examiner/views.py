''' Routes and View Functions for The Examiner user's functionalities'''
from app import db
from app.models import Quiz, Question
from datetime import date, time
from flask import flash, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from . import examiner

# Home page
@examiner.route('/examinerhome')
def examinerhome():
    return render_template('examiner/examiner_home.html')

# Render quiz list
@examiner.route('/quizlist')
@login_required
def quizlist():
    quizes = Quiz.query.filter_by(user_id=current_user.id).all()
    return render_template('examiner/quizlist.html', quizes=quizes)


# specific quiz
@examiner.route('/onequiz/<int:id>')
@login_required
def onequiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    return render_template('examiner/quiz_n.html', quiz=quiz)

# Add new quiz
@examiner.route('/addquiz', methods=['POST', 'GET'])
@login_required
def addquiz():
    if current_user.role != 'EXAMINER':
        return
    if request.method == 'POST':
        quiz_name = request.form['quizname']
        quiz_day = request.form['quizdate'].split('-')
        quiz_time = request.form['quiztime'].split(':')
        
        
        day = date(int(quiz_day[0]), int(quiz_day[1]), int(quiz_day[2]))
        tim = time(int(quiz_time[0]), int(quiz_time[1]))
        
        try:
            quiz = Quiz(name=quiz_name, date=day, time=tim, user_id=current_user.id)
            
            db.session.add(quiz)
            db.session.commit()
            flash("Success")
        except Exception as e:
            flash("{}".format(str(e)))        
            db.session.rollback()
    return redirect(url_for('examiner.examinerhome'))