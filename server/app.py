#!/usr/bin/env python3

from flask import Flask, make_response, abort
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config points to our existing database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #set to false to avoid building up too much unhelpful data in memory when the application is running

migrate = Migrate(app, db) #migrate instance configures the application and models for Flask-Migrate
db.init_app(app) #connects the application to the database

@app.route('/') #determines there is a view available at '/' and saves it to our URL map
def index():
    res = make_response('<h1>Welcome to the pet/owner directory!</h1>', 200)

    return res

@app.route('/pets')
def all_pets():
    pets = Pet.query.all()
    # response = f'{[pet.name for pet in pets]}'
    response = '<h1>hello world</h1>'
    return make_response(response, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        response = f'''
            <h1>Information for {pet.name}</h1>
            <h2>Pet species: {pet.species}</h2>
            <h3>Pet owner: {pet.owner.name}</h3>
        '''
        return make_response(response, 200)
    else:
        abort(404)


@app.route('/owners/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()
    if owner:
        response = f'<h1>Information for {owner.name}</h1>'
        pet_res = '<h2> has no pets at this time </h2>'
        pets = [pet for pet in owner.pets]
        if pets:
            pet_res = ""
            for pet in pets:
                pet_res += f'''<h2> {owner.name} has a pet {pet.species} named {pet.name} </h2>'''
        
        response += pet_res
        return make_response(response, 200)
    else:
        return abort(404)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
