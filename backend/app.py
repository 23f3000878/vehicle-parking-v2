from controllers import blueprints
from controllers.admin import create_admin
from config import Config
from flask import Flask
from flask_jwt_extended import JWTManager
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
import os
from extensions import db, mail, cache
from flask_cors import CORS
from celery_app import  make_celery

# Enable cascading deletes in SQLite
@event.listens_for(Engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
cache.init_app(app)
mail.init_app(app)
make_celery(app)
app.app_context().push()


# Register all blueprints
for bp in blueprints:
    app.register_blueprint(bp)

# Create EXPORT_DIR if not exists
os.makedirs(app.config['EXPORT_DIR'], exist_ok=True)

if(__name__=='__main__'):
    db.create_all()
    create_admin()
    app.run(
    debug=True,
    port=8080,
    host='0.0.0.0'
    )