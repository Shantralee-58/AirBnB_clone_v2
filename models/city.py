#!/usr/bin/python3
""" """
from models.base_model import BaseModel, Base
from models.place import Place
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    __tablename__ = "cities"

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    places = relationship("Place", backref="cities", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initiate the instance with some default values and call the
        super init to complete the initiate
        """
        super().__init__(*args, **kwargs)
