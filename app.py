from model import db
from controllers import create_admin,blueprints
from config import Config
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
jwt.init_app(app)

app.config.from_object(Config)
db.init_app(app)
app.app_context().push()

# Register all blueprints
for bp in blueprints:
    app.register_blueprint(bp)

if(__name__=='__main__'):
    db.create_all()
    create_admin()
    app.run(
    debug=True,
    port=8080,
    host='0.0.0.0'
    )