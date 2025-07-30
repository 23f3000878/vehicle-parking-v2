from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timezone
from extensions import db

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    address = db.Column(db.String,nullable=True)
    password = db.Column(db.String,nullable=False)
    fullname = db.Column(db.String,nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='role'), default='user')
    reserved_spots = db.relationship('ReserveSpot', back_populates='user', cascade="all, delete-orphan", passive_deletes=True)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Lot(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.Integer,autoincrement=True,primary_key =True)
    name= db.Column(db.String,nullable=False,unique=True)
    prime_location_name = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    address = db.Column(db.String,nullable=False)
    pincode = db.Column(db.Integer,nullable=False)
    no_of_spots = db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.now(timezone.utc))
    spots=db.relationship('Spot',back_populates='lot',cascade="delete", passive_deletes=True)

class Spot(db.Model):
    __tablename__ = 'spot'
    id = db.Column(db.Integer,autoincrement=True,primary_key =True)
    lot_id = db.Column(db.Integer,db.ForeignKey("lot.id",ondelete="CASCADE"))
    lot=db.relationship('Lot',back_populates='spots')
    spot_number = db.Column(db.Integer,nullable=False)
    status = db.Column(db.Enum('A', 'O', name='status'), default='A')
    created_at=db.Column(db.DateTime,default=datetime.now(timezone.utc))
    reserved_spots = db.relationship('ReserveSpot', back_populates='spot', cascade="all, delete-orphan", passive_deletes=True)

class ReserveSpot(db.Model):
    __tablename__='reserve_spot'
    id = db.Column(db.Integer,autoincrement=True,primary_key =True)
    spot_id = db.Column(db.Integer,db.ForeignKey("spot.id"))
    spot = db.relationship('Spot', back_populates='reserved_spots')
    user_id = db.Column(db.Integer,db.ForeignKey("user.id", ondelete="CASCADE"))
    user= db.relationship('User', back_populates='reserved_spots')
    vehicle_no = db.Column(db.String,nullable=False)
    parking_time=db.Column(db.DateTime,nullable=False)
    leaving_time=db.Column(db.DateTime,nullable=True)
    cost = db.Column(db.Float,nullable=True,default=0)
    location = db.Column(db.String,nullable=False)
