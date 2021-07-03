''' Authentication Routes '''
from app import db
from app.models import Student, Examiner, User
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, current_user
from .forms import RegisterForm, LoginForm
from . import auth, views



''' Create a new user '''
@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        
        user.fname = form.fname.data
        user.lname = form.lname.data
        user.email = form.email.data
        user.password = form.password.data
        user.role = form.role.data
               
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            flash("{}".format(str(e)))
            db.session.rollback()
            return render_template('register.html', form=form)
        
        person = User.query.filter_by(email=user.email).first() # database id of the above user
        
        # check for role of user and redirect to respective role's
        # endpoint for adding to database
        if user.role == 'STUDENT':
            return redirect(url_for('auth.addstudent', id=person.id))
        elif user.role == 'EXAMINER':
            return redirect(url_for('auth.addxaminer', id=person.id))
        else: 
            pass 
    else:
        return render_template('register.html', form=form)
        
''' create a new student from user created at /register '''
@auth.route('/addstudent/<int:id>', methods=['POST', 'GET'])
def addstudent(id):
    form = LoginForm()
    student = Student(student_user_id=id)  
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('index.html'))   

''' create a new examiner from user created at /register '''
@auth.route('/addexaminer/<int:id>', methods=['POST', 'GET'])
def addexaminer(id):
    form = LoginForm()
    examiner = Examiner(student_user_id=id)  
    db.session.add(examiner)
    db.session.commit()
    return redirect(url_for('index.html')) 

''' Login '''
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data
        
        user = User.query.filter_by(email=user_email).first()
        
        # verify provided creadentials
        if user is not None and user.verify_password(user_password):
            login_user(user)
    else:
        return redirect(url_for('index.html'))
    
    return 'Great, {}!'.format(current_user.fname)

@auth.route('/logout')
def logout():
    form = LoginForm()
    logout_user()
    return redirect(url_for('main.index'))
            
            
        
        
  
