from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timezone
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    fullname = db.Column(db.String(100), nullable = False)
    reservations = db.relationship('Reservation', backref= 'user' , lazy= True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self , password):
        return bcrypt.check_password_hash(self.password , password)
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False , default="admin@gmail.com")
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255) , nullable = False , default = "Admin")

    def set_password(self , password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self , password):
        return bcrypt.check_password_hash(self.password , password)

class ParkingLot(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    location_name = db.Column(db.String(150) , nullable = False)
    price_per_hour = db.Column(db.Float , nullable = False)
    address = db.Column(db.String(264), nullable= False)
    pincode = db.Column(db.String(6), nullable= False)
    no_of_spots = db.Column(db.Integer , nullable= False)
    spots = db.relationship('ParkingSpot', backref='lot' , lazy= True)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), default='A')  # A = Available, O = Occupied
    reservations = db.relationship('Reservation', backref='spot', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    parking_timestamp = db.Column(db.DateTime(timezone=True), nullable=True)
    leaving_timestamp = db.Column(db.DateTime(timezone=True), nullable=True)
    parking_cost = db.Column(db.Float, default=0.0)