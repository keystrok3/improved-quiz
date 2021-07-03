
from . import auth
from .exceptions import ValidationError

@auth.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
