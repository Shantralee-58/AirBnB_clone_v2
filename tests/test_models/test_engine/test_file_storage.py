#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models import storage
import os


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Using DB not FileStorage")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

        self.file_path = storage._FileStorage__file_path

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove(self.file_path)
        except Exception:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        import copy

        objects_before = copy.deepcopy(storage.all())
        new = BaseModel()
        new.save()
        objects = storage.all()

        self.assertTrue(len(objects) > len(objects_before))

        for obj in objects.values():
            temp = obj
        self.assertTrue(temp is new)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_all_with_class(self):
        """ Test FileStorage.all(self, cls) with a class
        """
        inst_1 = User()
        inst_1.save()
        inst_2 = User()
        inst_2.save()
        inst_3 = State()
        inst_3.save()

        result = storage.all(User)

        self.assertTrue(inst_1 in result.values())
        self.assertTrue(inst_2 in result.values())
        self.assertFalse(inst_3 in result.values())

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists(self.file_path))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize(self.file_path), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists(self.file_path))
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.assertTrue(f"BaseModel.{new.id}" in f.read())

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        import copy

        new = BaseModel()
        new.save()
        self.setUp()  # clear the storage. __objects

        storage.reload()
        objects_after = storage.all()
        self.assertTrue(len(objects_after) > 0)
        self.assertTrue(f"BaseModel.{new.id}" in objects_after)

    def test_reload_empty(self):
        """ Load from an empty file """
        with open(self.file_path, 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        new.save()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)
        