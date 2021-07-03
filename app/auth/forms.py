''' WTForms form classes '''

from app.models import User
from .exceptions import ValidationError
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email

class RegisterForm(Form):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired(), 
                                                EqualTo('password', message='Passwords must match')])
    role = SelectField('Role', choices=['STUDENT', 'EXAMINER'])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
    

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
