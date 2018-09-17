from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/restaurants/')
def showRestaurants():
    return render_template('showrestaurants.html')


@app.route('/restaurant/new')
def createRestaurant():
    return render_template('createrestaurant.html')


if __name__ =="__main__":
    app.run(debug=True)    
