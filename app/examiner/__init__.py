''' Examiner blueprint '''
from flask import Blueprint

examiner = Blueprint('examiner', __name__)

from . import views