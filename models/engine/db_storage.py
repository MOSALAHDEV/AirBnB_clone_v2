#!usr/bin/python3
""" This file is db storage for hbnb clone """
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = {
    'User': User,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review
}

class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes DBStorage """
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, database), pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        
    def all(self, cls=None):
        """ Returns a dictionary of models currently in storage """
        self.reload()
        new_dict = {}
        if cls is None:
                for c in classes.values():
                    objs = self.__session.query(c).all()
                    for obj in objs:
                        key = obj.__class__.__name__ + '.' + obj.id
                        new_dict[key] = obj
        else:
            if cls in classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, cls=None):
        """ Adds an object to the current database session """
        self.__session.add(cls)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, cls=None):
        """ Deletes an object from the current database session """
        if cls is not None:
            self.__session.delete(cls)

    def reload(self):
        """ Creates all tables in the database and creates a session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
    
    def count(self, cls=None):
        """ Counts objects in storage """
        if cls is None:
            count = 0
            for c in classes.values():
                count += self.__session.query(c).count()
        else:
            count = self.__session.query(cls).count()
        return count
