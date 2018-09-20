from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Restaurant, Menu

import os
from random import randint

import logging
from forms import RestaurantForm

import models


baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEVELOPMENT'] = True
app.config['SECRET_KEY'] = "super secret key"

engine = create_engine('sqlite:///marcorestaurant.db', echo=True)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

menu = [
    {'id':1, 'name': 'Chicken Tikka Masala', 'price': '10.99', 'description': 'Tender pieces of boneless marinated chicken roasted in a clay oven & cooked in a creamy tomato gravy', 'restaurant_id':2},
    {'id':2, 'name': 'Chicken Biriyani', 'price': '11.99', 'description': 'Basmati rice cooked with chicken and flavored with cardamom, saffron and Indian herb','restaurant_id':1},
    {'id':3, 'name': 'Beef Biriyani', 'price': '11.99', 'description': 'Succulent pieces of beef cooked with basmati rice over a low fire with exotic Indian herbs and spice', 'restaurant_id':2},
    {'id':4, 'name': 'Goat Biriyani', 'price': '15.99', 'description': 'Tender pieces of goat cooked with basmati rice over a low fire with exotic Indian herbs and spice','restaurant_id':1},
    {'id':5, 'name': 'Mughlai Vegetable Biryani', 'price': '11.99', 'description': 'Basmati rice cooked with seasonal vegetables and flavored with saffron and spice', 'restaurant_id':2}

]

# def store_restaurants(rest_id, name, location):
#     restaurants.append(dict(
#         id=rest_id,
#         name = name,
#         location = location
#         )
#     )


# def find_No_duplicate(rest_id, restaurants):
#     for rest in restaurants:
#         if id == rest_id:
#             return False
#         else:
#             return True
    


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# ===============================  Restaurant ================================= #

@app.route('/restaurants/')
def showRestaurants():
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    session.close()
    return render_template('showrestaurants.html', restaurants = restaurants)


@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    session.close()
    return jsonify(Restaurants=[i.serializeRestaurant for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>')
def viewRestaurantDetails(restaurant_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(Menu).filter_by(restaurant_id = restaurant.id).all()
    session.close()
    return render_template('viewrestaurantdetails.html', restaurant=restaurant, menus = menuItems)



@app.route('/restaurant/new', methods=['GET', 'POST'])
def createRestaurant():
    session = DBSession()
    form = RestaurantForm()
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        description = form.description.data
        restaurant = models.Restaurant(name=name, location =location, description = description)
        session.add(restaurant)
        session.commit()
        session.close()
        flash("Added '{}'".format(name))
        return redirect(url_for('showRestaurants'))

    return render_template('createrestaurant.html', form=form)



session.close()


if __name__ =="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))  
    app.run(debug=True)
