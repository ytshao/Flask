
from flask import Flask, json, jsonify, abort, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.restless import APIManager

app = Flask(__name__)

app.config.from_pyfile('Config.py')

# Database component

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

    def to_dict(self):
        return {"Lastname":self.Lastname, "Firstname":self.Firstname, "Facebook_id":self.Facebook_id, "Credits":self.Credits, "Scores":self.Scores, "Number_of_scores":self.Number_of_scores, "Number_of_runs":self.Number_of_runs, "Give_current":self.Give_current, "Receive_current":self.Receive_current}
    
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

    def to_dict(self):
        return {"Restaurant_id":self.Restaurant_id, "date":self.date, "slot_time":self.slot_time, "Rest_slot":self.Rest_slot}


# API Functions
@app.route('/restaurants/findbyid/<int:id>/', methods = ['GET'])
def get_rest(id):    
    query = Restaurants.query.filter_by(id=id).all()
    return json.dumps([obj.to_dict() for obj in query])


@app.route('/restaurants/findbyname/<name>/', methods = ['GET'])
def get_rest_name(name):
    query = Restaurants.query.filter_by(Name=name).all()
    return json.dumps([obj.to_dict() for obj in query])


@app.route('/users/findbyid/<facebook_id>/', methods= ['GET'])
def get_user(facebook_id):
    query = Users.query.filter_by(Facebook_id=facebook_id).all()
    return json.dumps([obj.to_dict() for obj in query])


@app.route('/restaurants/', methods = ['GET'])
def get_rest_all():
    query = Restaurants.query.all()
    return json.dumps([obj.to_dict() for obj in query])


@app.route('/users/', methods = ['GET'])
def get_user_all():
    query = Users.query.all()
    return json.dumps([obj.to_dict() for obj in query])


@app.route('/auctionhouse/', methods = ['GET'])
def get_auctionhouse_all():
    query = Auctionhouse.query.all()
    return json.dumps([obj.to_dict() for obj in query])


@app.route('/restaurants/posts/', methods = ['POST'])
def create_rest():
    #error check
    if not request.json or not 'Name' in request.json:
        abort(400)

    rest = Restaurant(request.json.get('Name',''), request.json.get('City',''), request.json.get('Neighborhood',''), request.json.get('Address',''), request.json.get('Picture_url',''), request.json.get('Latitude',''), request.json.get('Longitude',''), request.json.get('Rating',''), request.json.get('Review_Count',''), request.json.get('Phone',''), request.json.get('Rest_key',''))

    db.session.add(rest)
    db.session.commit()

    return jsonify({'restaurant': rest}), 201


@app.route('/restaurants/<int:id>', methods = ['DELETE'])
def delete_rest(id):
    
    db.session.delete(Restaurants.query.get(id))
    db.session.commit()

    return jsonify({'result': True})


@app.route('/restaurants/put/<int:id>', methods = ['PUT'])
def update_rest(id):
    rest = Restaurants.query.get(id)

    rest.Name = request.json.get('Name', rest.Name)
    rest.City = request.json.get('City', rest.City)
    rest.Neighborhood = request.json.get('Neighborhood', rest.Neighborhood)
    rest.Address = request.json.get('Address', rest.Address)
    rest.Picture_url = request.json.get('Picture_url', rest.Picture_url)
    rest.Latitude = request.json.get('Latitude', rest.Latitude)
    rest.Longitude = request.json.get('Longitude', rest.Longitude)
    rest.Rating = request.json.get('Rating', rest.Rating)
    rest.Review_Count = request.json.get('Review_Count', rest.Review_Count)
    rest.Phone = request.json.get('Phone', rest.Phone)
    rest.Rest_key = request.json.get('Rest_key'. rest.Rest_key)

    db.session.commit()

    return json.dumps(rest.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
