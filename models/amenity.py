#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String 
from os import getenv
from sqlalchemy.orm import relationship
import sqlalchemy



class Amenity(BaseModel, Base):
    """ Amenity class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializing amenity from base model"""
        super().__init__(*args, **kwargs)
