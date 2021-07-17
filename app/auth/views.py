''' Authentication Routes '''
from app import db
from app.models import User
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, current_user
from .forms import RegisterForm, LoginForm
from . import auth



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
    else:
        return render_template('register.html', form=form)
    
    return redirect(url_for('main.index'))

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
        
        if current_user.role == 'EXAMINER':
            return redirect(url_for('examiner.examinerhome'))
        elif current_user.role == 'STUDENT':
            return redirect(url_for('student.studenthome'))
    else:
        return redirect(url_for('main.index'))
    
# log out route
@auth.route('/logout')
def logout():
    form = LoginForm()
    logout_user()
    return redirect(url_for('main.index'))
            
            
        
        
  
