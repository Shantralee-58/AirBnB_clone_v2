#!/usr/bin/python3
""" """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, aliased
import os


class State(BaseModel, Base):
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # in databases systems
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        # Relationship with City
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    # in file_storage systems
    else:
        @property
        def cities(self):
            """ getter attribute that return all cities linked to this state
            """
            from models import storage
            cities = [city for city in storage.all(City).values()
                      if city.state_id == self.id]
            return cities

    def __init__(self, *args, **kwargs):
        """ Initiate the instance with some default values and call the
        super init to complete the initiate
        """
        super().__init__(*args, **kwargs)


aliased_state = aliased(State, name='state')
