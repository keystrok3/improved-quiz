''' Routes and View Functions for The Examiner user's functionalities'''
from app import db
from app.models import Quiz, Question, User
from datetime import date, time
from flask import flash, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from . import examiner
from .forms import QuestionForm

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
    form = QuestionForm()
    questions = Question.query.filter_by(quiz_id=id).all()
    quiz = Quiz.query.filter_by(id=id).first()
    students = User.query.filter_by(role='STUDENT').all()
    return render_template('examiner/quiz_n.html', form=form, questions=questions, quiz=quiz, students=students)

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

@examiner.route('/addquestion/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def addquestion(quiz_id):
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question()
        
        question.detail = form.detail.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.correct_option = form.correct_option.data
        question.quiz_id = quiz_id
        
        try:
            db.session.add(question)
            db.session.commit()
            flash("Success")
        except Exception as e:
            flash('{}'.form(str(e)))
    else:
        flash(form.errors['correct_option'])
    
    return redirect(url_for('examiner.onequiz', id=quiz_id))

    
    


    