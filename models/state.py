#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class State(BaseModel):
    """ State class """
    name = ""
    cities = []
    def __init__(self, *args, **kwargs):
        """Initializes a new State instance"""
        super().__init__(*args, **kwargs)
        if 'cities' in kwargs:
            self.cities = kwargs['cities']
