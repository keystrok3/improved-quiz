from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash

""" User models """

# Student Quiz Registrations Association Table
registrations = db.Table('registrations', 
                         db.Column('student_id', db.Integer, db.ForeignKey('students.id')), 
                         db.Column('quiz_id', db.Integer, db.ForeignKey('quizes.id')))



# Student model
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    quizes = db.relationship('Quiz', 
                            secondary=registrations,
                            backref=db.backref('students', lazy='dynamic'),
                            lazy='dynamic')
    
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Examiner model
class Examiner(db.Model):
    __tablename__ = "examiners"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    quizes = db.relationship('Quiz', backref='examiner')
    
    password_hash = db.Column(db.String(128))
    
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
    name = db.Column(db.String(64))
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiners.id'))
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
    student_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    solution = db.Column(db.String(64))
    

app = create_app('development')
app.app_context().push()
db.create_all()