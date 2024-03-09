#!/usr/bin/python3
"""storage module"""
import datetime
import json


class FileStorage:
    """File Storage class to handle file operations."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id"""
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file."""
        if len(self.__objects) > 0:
            new_dict = {}
            the_copy = self.__objects.copy()
            for key in the_copy:
                new_dict[key] = the_copy[key].to_dict()

        with open(self.__file_path, 'w', encoding="utf-8") as file:
            file.write(json.dumps(new_dict, indent=4))

    def reload(self):
        """Deserialize the JSON file to __objects."""
        from models.base_model import BaseModel
        from models.amenity import Amenity
        from city import City
        from place import Place
        from review import Review
        from state import State
        from user import User

        try:
            with open(self.__file_path, 'r', encoding="utf-8") as file:
                new = file.read()
                loaded_objects = json.loads(new)
                for key, value in loaded_objects.items():
                    class_name, obj_id = key.split('.')
                    # Convert datetime strings to datetime objects
                    value['created_at'] = datetime.datetime.strptime(
                            value['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
                    value['updated_at'] = datetime.datetime.strptime(
                            value['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
                    # Recreate BaseModel objects
                    obj = BaseModel(**value)
                    # Assign class name to obj
                    obj.__class__.__name__ = class_name
                    obj.id = obj_id  # Assign object ID to obj
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass
