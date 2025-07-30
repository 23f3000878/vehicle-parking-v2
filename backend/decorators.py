from functools import wraps
from flask import abort, g
from model import User
from flask_jwt_extended import get_jwt_identity, jwt_required

def login_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(401)
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function