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
