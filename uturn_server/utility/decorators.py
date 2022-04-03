from functools import wraps
from flask import abort, request
from . import token

def restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("uturn-access-key") != token:
                abort(403)
        return f(*args, **kwargs)
    return decorated_function