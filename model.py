from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    fullname = db.Column(db.String,nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='role'), default='user')
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Lot(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.Integer,autoincrement=True,primary_key =True)
    prime_location_name = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    address = db.Column(db.String,nullable=False)
    pincode = db.Column(db.Integer,nullable=False)
    no_of_spots = db.Column(db.Integer,nullable=False)
    spots=db.relationship('Spot',back_populates='lot')

class Spot(db.Model):
    __tablename__ = 'spot'
    id = db.Column(db.Integer,autoincrement=True,primary_key =True)
    lot_id = db.Column(db.Integer,db.ForeignKey("lot.id"))
    lot=db.relationship('Lot',back_populates='spots')
    status = db.Column(db.Enum('A', 'O', name='status'), default='A')

class ReserveSpot(db.Model):
    __tablename__='reserve_spot'
    id = db.Column(db.Integer,autoincrement=True,primary_key =True)
    spot_id = db.Column(db.Integer,db.ForeignKey("spot.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    vehicle_no = db.Column(db.String,nullable=False)
    parking_time=db.Column(db.String,nullable=False)
    leaving_time=db.Column(db.String,nullable=False)
    cost = db.Column(db.Float,nullable=False)