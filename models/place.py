#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
import models
import sqlalchemy


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        place_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializing place from base model"""
        super().__init__(*args, **kwargs)

    def reviews(self):
        """returns the list of Review instances"""
        reviews = models.storage.all(Review).values()
        review_list = []
        for review in reviews:
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity', Base.metadata, Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False), Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
        )

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            """returns the list of Amenity instances"""
            amenities = models.storage.all("Amenity").values
            amenity_list = []
            for amenity in amenities:
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
        
        @amenities.setter
        def amenities(self, obj):
            if not isinstance(obj, Amenity):
                return
            self.amenity_ids.append(obj.id)
