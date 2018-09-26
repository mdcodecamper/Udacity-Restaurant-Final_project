from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Restaurant, Menu

import os
from random import randint

import logging
from forms import RestaurantForm, MenuItemForm

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
    return render_template('restaurant/showrestaurants.html', restaurants = restaurants)


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
    return render_template('restaurant/viewrestaurantdetails.html', restaurant=restaurant, menus = menuItems)



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

    return render_template('restaurant/createrestaurant.html', form=form)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = DBSession()
    form = RestaurantForm()
    editedrestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if form.validate_on_submit():
        if request.form['name']:
            editedrestaurant.name = form.name.data
        if request.form['location']:
            editedrestaurant.location = form.location.data
        if request.form['description']:
            editedrestaurant.description = form.description.data
        session.add(editedrestaurant)
        session.commit()
        session.close()
        flash("Restaurant Edited Successfully!!! ")
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))

    return render_template('restaurant/editrestaurant.html', restaurant_id=restaurant_id, item=editedrestaurant, form=form)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = DBSession()
    form = RestaurantForm()
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if form.validate_on_submit():
        session.delete(restaurantToDelete)
        session.commit()
        session.close()
        flash("Restaurant Deleted Successfully!!! ")
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))

    return render_template('restaurant/deleterestaurant.html', item = restaurantToDelete, form=form)


# ===============================  Menu Item ================================= #

@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def createMenuItem(restaurant_id):
    session = DBSession()
    form = MenuItemForm()
    if form.validate_on_submit():
        name = form.name.data
        course = form.course.data
        category = form.category.data
        price = form.price.data
        description = form.description.data
        menuItem = models.Menu(name=name, course =course, category=category, description = description, price= price, restaurant_id=restaurant_id)
        session.add(menuItem)
        session.commit()
        session.close()
        flash("Added {} ".format(name))
        return redirect(url_for('viewRestaurantDetails', restaurant_id = restaurant_id))

    return render_template('menu/createmenu.html', form=form)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = DBSession()
    form = MenuItemForm()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editedMenu = session.query(Menu).filter_by(id=menu_id).one()
    if form.validate_on_submit():
        if request.form['name']:
            editedMenu.name = form.name.data
        if request.form['course']:
            editedMenu.course = form.course.data
        if request.form['category']:
            editedMenu.category = form.category.data
        if request.form['price']:
            editedMenu.price = form.price.data
        if request.form['description']:
            editedMenu.description = form.description.data
        session.add(editedMenu)
        session.commit()
        session.close()
        flash("Menu Item Successfully Edited")
        return redirect(url_for('viewRestaurantDetails', restaurant_id = restaurant_id))

    return render_template('menu/editmenu.html', restaurant_id = restaurant_id, menu_id=menu_id, item=editedMenu, form=form)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = DBSession()
    form = MenuItemForm()
    menuItemToDelete = session.query(Menu).filter_by(id=menu_id).one()
    if form.validate_on_submit():
        session.delete(menuItemToDelete)
        session.commit()
        session.close()
        flash("Menu Item Deleted Successfully!!! ")
        return redirect(url_for('viewRestaurantDetails', restaurant_id=restaurant_id))
    
    return render_template('menu/deletemenu.html', item = menuItemToDelete, form=form)


session.close()


if __name__ =="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))  
    app.run(debug=True)

# set FLASK_ENV=development  -- windows