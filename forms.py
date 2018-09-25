from flask_wtf import Form
from wtforms.fields import StringField

    
class RestaurantForm(Form):
    name = StringField('name')
    location = StringField('location')
    description = StringField('description')



class MenuItemForm(Form):
    name = StringField('name')
    category = StringField('category')
    course = StringField('course')
    price = StringField('price')
    description = StringField('description')