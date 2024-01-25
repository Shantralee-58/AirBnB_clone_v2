#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import Base, BaseModel
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, aliased
import os

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        nullable=False,
        primary_key=True,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        nullable=False,
        primary_key=True,
    ),
)


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    else:

        @property
        def reviews(self):
            """Return self.reviews"""
            from models import storage

            reviews = [
                rev for rev in storage.all(Review).values() if rev.place_id == self.id
            ]
            return reviews

        @property
        def amenities(self):
            """getter for self.amenities"""
            from models import storage

            return [
                amenity
                for amenity in storage.all(Amenity).values()
                if amenity.id in amenity_ids
            ]

        @amenities.setter
        def amenities(self, amenity):
            """setter for the self.amentities"""
            if not isinstance(amenity, Amenity):
                return
            amenity_ids.append(amenity.id)

    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initiate the instance with some default values and call the
        super init to complete the initiate
        """
        super().__init__(*args, **kwargs)


alaised_place = aliased(Place, "place")
