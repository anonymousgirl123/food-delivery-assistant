from sqlalchemy import Column, String, Integer, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    veg = Column(Boolean)
    preferred_cuisine = Column(String)


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cuisine = Column(String)
    price = Column(Integer)
    type = Column(String)
    category = Column(String)  # main / drink / side / dessert
