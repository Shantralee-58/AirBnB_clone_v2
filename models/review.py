#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """Review classto store review information"""

    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initiate the instance with some default values and call the
        super init to complete the initiate
        """
        super().__init__(*args, **kwargs)
