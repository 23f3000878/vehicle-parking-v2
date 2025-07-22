from flask import Flask,abort
from functools import wraps
from flask_jwt_extended import (
    get_jwt_identity
)
from model import db,User

#Blueprints
from .auth import auth_bp
from .user import user_bp
from .admin import admin_bp

# Export them so app.py can import from one place
blueprints = [
    auth_bp,
    user_bp,
    admin_bp
]

#Pre Creating Admin
def create_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin',role='admin',fullname='Admin',)
        admin.set_password('admin')  # Set a secure password
        db.session.add(admin)
        db.session.commit()

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if current_user.role!='admin':  # Check if the current user is an admin
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function