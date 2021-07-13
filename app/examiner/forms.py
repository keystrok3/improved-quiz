from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, AnyOf

class QuestionForm(Form):
    detail = StringField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = StringField('Solution', validators=[DataRequired()])
    submit = SubmitField('Add')
