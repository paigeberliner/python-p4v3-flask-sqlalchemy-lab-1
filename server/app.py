# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if earthquake:
        response_body = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        response_status = 200 
    else: 
        response_body = {
            'message': 'Earthquake 9999 not found.'
        }
        response_status = 404

    response = make_response(response_body, response_status)
    return response
   

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude > magnitude).all()
    if earthquakes:
        response_body = {
            "count": len(earthquakes),
            "quakes": [
                {
                    'id': earthquake.id,
                    'magnitude': earthquake.magnitude,
                    'location': earthquake.location,
                    'year': earthquake.year
                }
                for earthquake in earthquakes
            ]
        }
        response_status = 200
    else:
        response_body = {
            "count": 0,
            "quakes": []
        }
        response_status = 200

    
    response = make_response(response_body, response_status)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
