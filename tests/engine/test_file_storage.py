#!/usr/bin/python3
"""
Test for storage
"""
from datetime import datetime
import unittest
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Test FileStorage Class"""

    def setUp(self):
        """Set up method to create instances."""
        self.storage = FileStorage()

    def tearDown(self):
        """Tear down method to reset storage."""
        del self.storage

    def test_instance(self):
        """Check instantiation of FileStorage."""
        self.assertIsInstance(self.storage, FileStorage)

    def test_all(self):
        """Test the all() method."""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertEqual(all_objects, {})

    def test_new(self):
        """Test the new() method."""
        obj = BaseModel()
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.storage.new(obj)
        all_objects = self.storage.all()
        self.assertIn(key, all_objects)

    def test_save_reload(self):
        """Test save() and reload() methods."""
        obj = BaseModel()
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.storage.new(obj)
        self.storage.save()
        new_storage = FileStorage()
        new_storage.reload()
        all_objects = new_storage.all()
        self.assertIn(key, all_objects)

    def test_reload_nonexistent_file(self):
        """Test reload() with nonexistent file."""
        new_storage = FileStorage()
        new_storage.reload()
        all_objects = new_storage.all()
        self.assertEqual(all_objects, {})

    def test_reload_malformed_json(self):
        """Test reload() with malformed JSON."""
        with open(FileStorage._FileStorage__file_path, 'w') as f:
            f.write("This is not JSON.")
        new_storage = FileStorage()
        new_storage.reload()
        all_objects = new_storage.all()
        self.assertEqual(all_objects, {})

    if __name__ == '__main__':
        unittest.main()
