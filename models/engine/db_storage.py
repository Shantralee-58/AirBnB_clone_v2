#!/usr/bin/python3

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        from models.base_model import Base

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
            isolation_level="READ COMMITTED",
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        from models.amenity import Amenity
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.review import Review

        classes = [Amenity, User, Place, State, City, Review]
        if cls:
            objs = self.__session.query(cls)
        else:
            objs = []
            for c in classes:
                objs += self.__session.query(c)

        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in objs}

    def new(self, obj):
        if obj in self.__session:
            _obj = self.__session.merge(obj)
        else:
            self.__session.commit()
            self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj and obj in self.__session:
            self.__session.delete(obj)

    def reload(self):
        from models.base_model import Base
        from models.amenity import Amenity
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.review import Review

        Base.metadata.create_all(self.__engine)

        DBStorage.Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )

        self.__session = DBStorage.Session()
