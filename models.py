# configuration
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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







engine = create_engine('sqlite:///marcorestaurant.db')
Base.metadata.create_all(engine)