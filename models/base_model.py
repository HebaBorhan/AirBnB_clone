#!/usr/bin/python3
"""base module"""
import uuid
import datetime


class BaseModel:
    """creating Base class"""
    def __init__(self, *args, **kwargs):
        """defines all common attributes/methods for other classes"""
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            self.created_at = datetime.datetime.strptime(
                self.created_at, "%Y-%m-%dT%H:%M:%S.%f")
            self.updated_at = datetime.datetime.strptime(
                self.updated_at, "%Y-%m-%dT%H:%M:%S.%f")
            return
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def save(self):
        """saves object into the database"""
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """returns dict. containing all keys/values of __dict__ of instance"""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict

    def __str__(self):
        """printing str"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
