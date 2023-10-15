#!/usr/bin/python3
"""
BaseModel class: This class serves as the
base class for all our models in the application.
"""

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Base class for all related classes"""

    def __init__(self, *args, **kwargs):
        """
        __init__: Constructor method that either deserializes
        a serialized class or initializes a new instance.
        """
        # Initialize if no keyword arguments are passed
        if kwargs == {}:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return

    def __str__(self):
        """
        __str__: Override the string representation of self.
        """
        str_fmt = f"[{type(self).__name__}] ({self.id}) {self.__dict__}"
        return str_fmt

    def save(self):
        """
        save: Updates the last updated variable and saves to storage.
        """
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        to_dict: Returns a dictionary representation of self.
        """
        dic = {**self.__dict__}
        dic['__class__'] = type(self).__name__
        dic['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        dic['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return dic
