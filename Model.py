from flask.ext.sqlalchemy import SQLAlchemy

from flask import Flask, json, jsonify, request, abort

from flask.ext.httpauth import HTTPBasicAuth

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from passlib.apps import custom_app_context as pwd_context


# Database component

app = Flask(__name__)

app.config.from_pyfile('Config.py')

db = SQLAlchemy(app)


class Restaurants(db.Model):
    
    id = db.Column(db.Integer)
    Name = db.Column(db.String(50))
    City = db.Column(db.String(50))
    Neighborhood = db.Column(db.String(100))
    Address = db.Column(db.String(200))
    Picture_url = db.Column(db.String(100))
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Rating = db.Column(db.Float)
    Review_Count = db.Column(db.Integer)
    Phone = db.Column(db.Integer)
    Rest_key = db.Column(db.String(200), primary_key=True)

    def __init__(self, Name, City, Neighborhood, Address, Picture_url, Latitude,Longitude, Rating, Review_Count, Phone, Rest_key):
        self.Name = Name
        self.City = City
        self.Neighborhood = Neighborhood
        self.Address = Address
        self.Picture_url = Picture_url
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Rating = Rating
        self.Review_Count = Review_Count
        self.Phone = Phone
        self.Rest_key = Rest_key
        
    def to_dict(self):
        # return {"Name":self.Name, "City":self.City}
        return {"Name":self.Name, "City":self.City, "Neighborhood":self.Neighborhood, "Latitude":self.Latitude, "Longitude":self.Longitude, "Rating":self.Rating,"Review_Count":self.Review_Count, "Phone":self.Phone, "Rest_key":self.Rest_key}

class Users(db.Model):

    id = db.Column(db.Integer)
    Lastname = db.Column(db.String(50))
    Firstname = db.Column(db.String(50))
    Facebook_id = db.Column(db.String(100), primary_key=True)
    Password_hash = db.Column(db.String(100))
    Credits = db.Column(db.Integer)
    Scores = db.Column(db.Float)
    Number_of_scores = db.Column(db.Integer)
    Number_of_runs = db.Column(db.Integer)
    Give_current = db.Column(db.Boolean)
    Receive_current = db.Column(db.Boolean)


    def __init__(self, Lastname, Firstname, Facebook_id, Password_hash, Credits, Scores, Number_of_scores, Number_of_runs, Give_current, Receive_current):
        self.Lastname = Lastname
        self.Firstname = Firstname
        self.Facebook_id = Facebook_id
        self.Password_hash = Password_hash
        self.Credits = Credits
        self.Scores = Scores
        self.Number_of_scores = Number_of_scores
        self.Number_of_runs = Number_of_runs
        self.Give_current = Give_current
        self.Receive_current = Receive_current

    def to_dict(self):
        return {"Lastname":self.Lastname, "Firstname":self.Firstname,
                "Facebook_id":self.Facebook_id, "Password_hash":self.Password_hash,
                "Credits":self.Credits, "Scores":self.Scores, 
                "Number_of_scores":self.Number_of_scores, "Number_of_runs":self.Number_of_runs, 
                "Give_current":self.Give_current, "Receive_current":self.Receive_current}
    
    def hash_password(self, password):
        self.Password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd.context.verify(password, self.Password_hash)


    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['Facebook_id'])
        return user

   
class Auctionhouse(db.Model):

    id = db.Column(db.Integer)
    Restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    date = db.Column(db.Date)
    slot_time = db.Column(db.DateTime)
    Rest_slot = db.Column(db.String(100), primary_key=True)
    slot_taken = db.Column(db.Boolean)
    slot_completed = db.Column(db.Boolean)


    def __init__(self, Restaurant_id, date, slot_time, Rest_slot, slot_taken, slot_completed):
        self.Restaurant_id = Restaurant_id
        self.date = date
        self.slot_time = slot_time
        self.Rest_slot = Rest_slot
        self.slot_taken = slot_taken
        self.slot_completed = slot_completed
        


    def to_dict(self):
        return {"Restaurant_id":self.Restaurant_id, "date":self.date, "slot_time":self.slot_time, "Rest_slot":self.Rest_slot, "slot_taken":self.slot_taken, "slot_completed":self.slot_completed}
