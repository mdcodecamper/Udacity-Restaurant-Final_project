from flask import Flask, render_template, url_for, request, redirect, flash
import os
import logging

app = Flask(__name__)
app.config['DEVELOPMENT'] = True
app.config['SECRET_KEY'] = "super secret key"


restaurants=[]

def store_restaurants(name, location):
    restaurants.append(dict(
        name = name,
        location = location
        )
    )


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/restaurants/')
def showRestaurants():
    return render_template('showrestaurants.html', restaurants = restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def createRestaurant():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        store_restaurants(name, location)
        logging.debug('Stored Restaurant: ' + name)
        flash("'{}' Restaurant Added.".format(name))
        return redirect(url_for('showRestaurants'))
    return render_template('createrestaurant.html')


if __name__ =="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))  
