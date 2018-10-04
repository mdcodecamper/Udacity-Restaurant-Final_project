# configuration
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    location = Column(String(250), nullable = False)
    description = Column(String(250))

    @property
    def serializeRestaurant(self):
    #Return object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,    
            'description': self.description    
        }
        

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    course = Column(String(250))
    category = Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serializeMenu(self):
        #Return object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'course': self.course,
            'category':self.category,
            'description':self.description,
            'price':self.price,
                    
        }


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = True)
    email = Column(String(256), nullable = True, unique = True)
    phone = Column(String(10))
    username = Column(String(12), unique = True)
    password_hash = Column(String(256))

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, password_hash)

    @property
    def serialize(self):
        #Return object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone':self.phone,
            'username':self.username,
                    
        }



engine = create_engine('sqlite:///marcorestaurant.db')
Base.metadata.create_all(engine)