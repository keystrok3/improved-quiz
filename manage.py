
from app import create_app, db
from app.models import Student, Examiner, Quiz, Question
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

import os

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Student=Student, Examiner=Examiner, Quiz=Quiz, Question=Question)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()