from app import create_app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

""" User models """

# User model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    role = db.Column(db.String(64), db.CheckConstraint("role == 'STUDENT' or role == 'EXAMINER'"))
    password_hash = db.Column(db.String(128), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# Quizes
class Quiz(db.Model):
    __tablename__ = "quizes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz')    
    
    
# Questions
class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(128), nullable=False)
    option1 = db.Column(db.String(64), nullable=False)
    option2 = db.Column(db.String(64), nullable=False)
    option3 = db.Column(db.String(64), nullable=False)
    option4 = db.Column(db.String(64), nullable=False)
    correct_option = db.Column(db.String(64))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'))


# Student solutions
class StudentSolutions(db.Model):
    __tablename__ = 'studentsolutions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    solution = db.Column(db.String(64))
    
class Registrations(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'))

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app('development')
app.app_context().push()
db.create_all()