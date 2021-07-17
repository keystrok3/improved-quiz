
from . import student
from app import db
from app.models import User, Quiz, Registrations, Question, StudentSolutions
from flask import render_template, url_for, session, redirect, flash, request
from flask_login import current_user,  login_required

# Render Student Home
@student.route('/studenthome')
@login_required
def studenthome():
    
    students_quizes = Registrations.query.filter_by(user_id=current_user.id).all()
    
    quizes_ids = [i.quiz_id for i in students_quizes]
    
    quizes = [q for q in Quiz.query.all() if q.id in quizes_ids]
    
    return render_template('student/studenthome.html', quizes=quizes)


# Get a specific quiz and its questions and return the questions in 
# a pagination object
@student.route('/getquiz/<int:id>/<int:qn_id>')
@login_required
def getquiz(id, qn_id):
    pagination = Question.query.filter_by(quiz_id=id).paginate(page=qn_id, per_page=1, error_out=False)
    quiz = Quiz.query.filter_by(id=id).first()
    
    if 'quiz_id' in session:
        session['quiz_id'] = id
        session.modified = True
    else:
        session['quiz_id'] = id
        
    quiz_name = quiz.name
    return render_template('student/takequiz.html', pagination=pagination, quiz_name=quiz_name)

# Submit a student's solution to a specific question
# on a specific quiz
@student.route('/addsolution/<int:qn_id>', methods=['POST', 'GET'])
@login_required
def addsolution(qn_id):
    if request.method == 'POST':
        quiz_id = session.get('quiz_id')
        student_solution = request.form.get('option')
        
        
        question = Question.query.filter_by(id=qn_id).first()
        correct_ans = question.correct_option
        
        # Check if solution is correct and set 
        # boolean to a variable to be sent to db
        iscorrect = None
        if student_solution == correct_ans:
            iscorrect = True
        else:
            iscorrect = False
        
        solution = StudentSolutions(user_id=current_user.id, question_id=qn_id, solution=student_solution, correct=iscorrect)
        
        try:
            db.session.add(solution)
            db.session.commit()
            flash('Done')
        except Exception as e:
            print('{}'.format(str(e)))    
            db.session.rollback()
    
    return redirect(url_for('student.getquiz', id=quiz_id, qn_id=qn_id))