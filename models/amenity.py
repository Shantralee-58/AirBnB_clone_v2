#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import Table, Column, String


class Amenity(BaseModel, Base):
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initiate the instance with some default values and call the
        super init to complete the initiate
        """
        super().__init__(*args, **kwargs)
