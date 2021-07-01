from . import main
from flask import render_template, url_for
from ..auth.forms import RegisterForm, LoginForm

""" Render Registration and Login templates  """

@main.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@main.route('/register', methods=['GET'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)