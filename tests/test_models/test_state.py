#!/usr/bin/python3
"""Test module for the State class using unittest module
"""
from tests.test_models.test_base_model import TestBaseModel
from models.state import State
from models.base_model import Base
from models import storage
import unittest
import os
import MySQLdb


class test_state(TestBaseModel):
    """subClass of unittest to test State class """

    def __init__(self, *args, **kwargs):
        """ Init the state test class and its super"""
        super().__init__(*args, **kwargs)

        # Retrieve MySQL connection parameters from environment variables
        host = os.getenv("HBNB_MYSQL_HOST")
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        db = os.getenv("HBNB_MYSQL_DB")

        # Check if any parameter is None and set default values if needed
        host = host or "localhost"
        user = user or "root"
        passwd = passwd or ""
        db = db or "test_db"

        # Establish the MySQL connection
        self.db = MySQLdb.connect(
            host=host,
            port=3306,
            user=user,
            passwd=passwd,
            database=db
        )

        self.cur = self.db.cursor()

        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Test the State name attribute"""
        new = self.value(name="Khar")
        self.assertEqual(type(new.name), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "file_storage",
                     "Test only on the file storage")
    def test_state_cities(self):
        """ Test the cities relatioship with the state in file_storage system
        """

        from models.city import City

        state = State()
        state.name = "kh"
        c_1 = City()
        c_1.state_id = state.id
        c_1.name = "Um"
        c_2 = City()
        c_2.name = "Bh"
        c_2.state_id = state.id

        state.save()
        c_1.save()
        c_2.save()

        cities = state.cities
        self.assertTrue(c_1.id in [city.id for city in cities])
        self.assertTrue(c_2.id in [city.id for city in cities])

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                     "Test only on the database storage systems")
    def test_state_cities(self):
        """ Test the cities relatioship with the state in database system
        """
        from models.city import City

        Base.metadata.drop_all(storage._DBStorage__engine)
        Base.metadata.create_all(storage._DBStorage__engine)

        state = State()
        state.name = "Kh"
        c_1 = City()
        c_1.name = "UM"
        c_2 = City()
        c_2.name = "BH"
        state.cities = [c_1, c_2]

        state.save()

        self.cur.execute("SELECT id, state_id FROM cities")

        results = self.cur.fetchall()

        self.assertTrue(state.id in results[0])
        self.assertTrue(c_1.id in results[0])
        self.assertTrue(state.id in results[1])
        self.assertTrue(c_2.id in results[1])

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                     "Test only on the database storage systems")
    def test_state_cities_relations(self):
        """ Test the relationship between state and ccities in
        a database system
        """
        from models import storage
        from models.city import City

        Base.metadata.drop_all(storage._DBStorage__engine)
        Base.metadata.create_all(storage._DBStorage__engine)

        state = State()
        state.name = "Kh"
        c_1 = City()
        c_1.name = "UM"
        c_2 = City()
        c_2.name = "BH"
        state.cities = [c_1, c_2]

        state.save()
        storage._DBStorage__session.delete(state)
        storage._DBStorage__session.commit()

        self.cur.execute("SELECT id, state_id FROM cities")

        self.assertTrue(len(self.cur.fetchall()) == 0)
