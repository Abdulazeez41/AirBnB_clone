#!/usr/bin/python3
"""
    Defines unittests for models/base_model.py.
"""

import unittest
from datetime import datetime, timedelta
from models import storage
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        """Set up for each test."""
        self.model = BaseModel()

    def tearDown(self):
        """Clean up after each test."""
        storage.delete_all()

    def test_instance_attributes(self):
        """Test instantiation and attributes."""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsNotNone(self.model.id)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str_representation(self):
        """Test the __str__ method."""
        expected_str = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected_str)

    def test_save_method(self):
        """Test the save method."""
        original_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, original_updated_at)

    def test_to_dict_method(self):
        """Test the to_dict method."""
        expected_dict = {
            'id': self.model.id,
            '__class__': 'BaseModel',
            'created_at': self.model.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'updated_at': self.model.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        }
        self.assertEqual(self.model.to_dict(), expected_dict)

    def test_deserialization(self):
        """Test deserialization of a BaseModel instance."""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(self.model.id, new_model.id)
        self.assertEqual(self.model.created_at, new_model.created_at)
        self.assertEqual(self.model.updated_at, new_model.updated_at)

    def test_update_method(self):
        """Test the update method."""
        original_created_at = self.model.created_at
        self.model.update(updated_at=datetime.utcnow())
        self.assertNotEqual(self.model.created_at, original_created_at)

    def test_destroy_method(self):
        """Test the destroy method."""
        model_id = self.model.id
        BaseModel.destroy(model_id)
        self.assertIsNone(storage.find_by_id('BaseModel', model_id))

    def test_class_methods(self):
        """Test class methods."""
        # Create new instance
        new_id = BaseModel.create()
        self.assertIsNotNone(new_id)
        new_model = storage.find_by_id('BaseModel', new_id)
        self.assertIsInstance(new_model, BaseModel)

        # Show instance
        shown_model = BaseModel.show(new_id)
        self.assertEqual(shown_model, new_model)

        # Count instances
        initial_count = BaseModel.count()
        BaseModel.create()
        new_count = BaseModel.count()
        self.assertEqual(new_count, initial_count + 1)

        # Retrieve all instances
        all_models = BaseModel.all()
        self.assertEqual(len(all_models), new_count)


if __name__ == '__main__':
    unittest.main()
