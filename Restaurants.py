
from flask import Flask, json, jsonify, abort, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.restless import APIManager

app = Flask(__name__)

app.config.from_pyfile('Config.py')

# Here we are making our database!
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
        


class Users(db.Model):
    id = db.Column(db.Integer)
    Lastname = db.Column(db.String(50))
    Firstname = db.Column(db.String(50))
    Facebook_id = db.Column(db.String(100), primary_key=True)
    Credits = db.Column(db.Integer)
    Scores = db.Column(db.Float)
    Number_of_scores = db.Column(db.Integer)
    Number_of_runs = db.Column(db.Integer)
    Give_current = db.Column(db.Boolean)
    Receive_current = db.Column(db.Boolean)

    def __init__(self, Lastname, Firstname, Facebook_id, Credits, Scores, Number_of_scores, Number_of_runs, Give_current, Receive_current):
        self.Lastname = Lastname
        self.Firstname = Firstname
        self.Facebook_id = Facebook_id
        self.Credits = Credits
        self.Scores = Scores
        self.Number_of_scores = Number_of_scores
        self.Number_of_runs = Number_of_runs
        self.Give_current = Give_current
        self.Receive_current = Receive_current

class Auctionhouse(db.Model):
    id = db.Column(db.Integer)
    Restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    date = db.Column(db.Date)
    slot_time = db.Column(db.DateTime)
    Rest_slot = db.Column(db.String(100), primary_key=True)

    def __init__(self, Restaurant_id, date, slot_time, Rest_slot):
        self.Restaurant_id = Restaurant_id
        self.date = date
        self.slot_time = slot_time
        self.Rest_slot = Rest_slot


@app.route('/rest/findbyid/<int:id>/', methods = ['GET'])
def get_rest(id):    
    query = Restaurants.query.filter_by(id=id).first()
    return jsonify({'stuff':query})
    # return jsonify({'restaurant_name':query.Name, 'restaurant_address':query.Address, 'phone':query.Phone})

@app.route('/rest/', methods = ['GET'])
def get_all():
    return jsonify({'restaurants': Restaurants.query.all()})

@app.route('/rest/', methods = ['POST'])
def create_rest():
    #error check
    if not request.json or not 'name' in request.json:
        abort(400)

    rest = Restaurant(request.json.name, request.json.get('visitDate',''), request.json.get('reviews',''))

    db.session.add(rest)
    db.session.commit()

    return jsonify({'restaurant': rest}), 201


@app.route('/rest/<int:id>', methods = ['DELETE'])
def delete_rest(id):
    
    db.session.delete(Restaurants.query.get(id))
    db.session.commit()

    return jsonify({'result': True})


@app.route('/rest/<int:id>', methods = ['PUT'])
def update_rest(id):
    rest = Restaurants.query.get(id)

    rest.name = request.json.get('name', rest.name)
    rest.visitDate = request.json.get('visitDate', rest.visitDate)
    rest.reviews = request.json.get('reviews', rest.reviews)

    db.session.commit()

    return jsonify( { 'rest': rest})


if __name__ == '__main__':
    app.run(debug=True)
