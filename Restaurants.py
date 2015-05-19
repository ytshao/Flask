
from flask import Flask, jsonify, abort, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.restless import APIManager

app = Flask(__name__)

app.config.from_pyfile('Config.py')

# Here we are making our database!
db = SQLAlchemy(app)

class Restaurants(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    visitDate = db.Column(db.Date)
    reviews = db.Column(db.Float)

    def __init__(self, name, visitDate, reviews):
        self.name = name
        self.hireDate = datetime.datetime.strptime(visitDate, "%d%m%Y").date()
        self.reviews = reviews



@app.route('/rest/', methods = ['GET'])

def get_rest(id):    
    return jsonify({'Restaurants': Restaurants.query.get(id)})



@app.route('/rest/<int:id>/', methods = ['GET'])

def get_all():
    return jsonify({'Restaurants': Restaurants.query.all()})



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
