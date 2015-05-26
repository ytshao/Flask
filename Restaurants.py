
from flask import Flask, json, jsonify, abort, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.restless import APIManager

from Model import *

from Superpass import superpass

from passlib.apps import custom_app_context as pwd_context

# API Functions

auth = HTTPBasicAuth()

# GET requests

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

# POST requests

@app.route('/restaurants/', methods = ['POST'])
def create_rest():
    #error check
    if not request.json or not 'Name' in request.json:
        abort(400)

    rest = Restaurants(request.json.get('Name',''), request.json.get('City',''),
            request.json.get('Neighborhood',''), request.json.get('Address',''),
            request.json.get('Picture_url',''), request.json.get('Latitude',0.0),
            request.json.get('Longitude',0.0), request.json.get('Rating',0.0), 
            request.json.get('Review_Count',0), request.json.get('Phone',0),
            request.json.get('Rest_key',''))

    # print rest
    db.session.add(rest)
    db.session.commit()

    return json.dumps(rest.to_dict()), 201

@app.route('/users/', methods = ['POST'])
def new_user():
    # error check
    if not request.json or not 'Username' in request.json:
        abort(400)

    username = request.json.get('Username')
    password = request.json.get('Password')
    
    if username is None or password is None:
        print "Problem 1"
        abort(400) # missing arguments
    if Users.query.filter_by(Facebook_id = username).first() is not None:
        print "Problem 2"
        abort(400) # existing user
    user = Users(Facebook_id = username, Password_hash = password,
            Lastname = request.json.get('Lastname',''), Firstname = request.json.get('Firstname',''), 
            Credits = 0, Scores = 0.0, Number_of_scores = 0, 
            Number_of_runs = 0, Give_current = 0, Receive_current = 0)
    
    user.hash_password(password)
    
    db.session.add(user)
    db.session.commit()

    return json.dumps(user.to_dict())

@app.route('/auctionhouse/', methods = ['POST'])
def new_entry():
    if not 'Restaurant_id' in request.json or not 'slot_time' in request.json:
        abort(400) # Insufficient information provided

    
    entry = Auctionhouse(Restaurant_id = request.json.get('Restaurant_id'),
                        date = request.json.get('date'),
                        slot_time = request.json.get('slot_time'),
                        Rest_slot = '', slot_taken = 0, slot_completed = 0)
    
    entry.Rest_slot = str(entry.Restaurant_id) + str(entry.date) + str(entry.slot_time)
    
    db.session.add(entry)
    db.session.commit()

    return json.dumps(entry.to_dict())


# DELETE requests

@app.route('/restaurants/<int:id>', methods = ['DELETE'])
def delete_rest(id):
    
    db.session.delete(Restaurants.query.get(id))
    db.session.commit()

    return jsonify({'result': True})

@app.route('/users/<facebook_id>', methods = ['DELETE'])
def delete_user(facebook_id):
    
    # Need to enter super user and password to get authorized
    super_user = request.json.get('Super_user')
    super_password = request.json.get('Super_password')
    
    if super_user is None or super_password is None:
        abort(400) # No Authorization
    if not pwd.context.encrypt(super_password) == superpass:
        abort(400) # Super_password is wrong
    else:
        db.session.delete(Users.query.get(facebook_id))
        db.session.commit()

    return jsonify({'result': True})

@app.route('/auctionhouse/<Rest_slot>', methods = ['DELETE'])
def delete_entry(Rest_slot):

    db.session.delete(Auctionhouse.query.get(Rest_slot))
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

# Should need authorization to update
@app.route('/users/put/<facebook_id>', methods = ['PUT'])
def update_user(facebook_id):
    user = Users.query.get(facebook_id)
    super_user = request.json.get('Super_user')
    super_password = request.json.get('Super_password')
    
    if super_user is None or super_password is None:
        user.Lastname = request.json.get('Lastname', user.Lastname)
        user.Firstname = request.json.get('Firstname', user.Firstname)

    if not pwd.context.encrypt(super_password) == superpass:
        abort(400) # Super_password is wrong
    else:
        user.Lastname = request.json.get('Lastname', user.Lastname)
        user.Firstname = request.json.get('Firstname', user.Firstname)
        user.Credits = request.json.get('Credits', user.Credits)
        user.Scores = request.json.get('Scores', user.Scores)
        user.Number_of_scores = request.json.get('Number_of_scores', user.Number_of_scores)
        user.Number_of_runs = request.json.get('Number_of_runs', user.Number_of_runs)
        user.Give_current = request.json.get('Give_current', user.Give_current)
        user.Receive_current = request.json.get('Receive_current', user.Number_of_scores)

    db.session.commit()

    return json.dumps(user.to_dict())

@app.route('/auctionhouse/put/<Rest_slot>', methods = ['PUT'])
def update_entry(Rest_slot):
    # Cannot change slot's restaurant name
    entry = Auctionhouse.query.get(Rest_slot)
    entry.date = request.json.get('date', entry.date)
    entry.slot_time = request.json.get('slot_time', entry.slot_time)
    entry.slot_taken = request.json.get('slot_taken', entry.slot_taken)
    entry.slot_completed = request.json.get('slot_completed', entry.slot_completed)

    # Now update Primary key
    entry.Rest_slot = str(entry.Restaurant_id) + str(entry.date) + str(entry.slot_time)
    
    db.session.commit()

    return json.dumps(entry.to_dict())

@app.route('/users/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token':token.decode('ascii') })

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Users.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


if __name__ == '__main__':
    app.run(debug=True)
