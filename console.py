#!/usr/bin/python3
"""
console.py module: Contains the entry point of the command interpreter.
"""

import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class: The command interpreter class which inherits from cmd.Cmd.
    """
    prompt = '(hbnb) '

    class_dict = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass

    def do_create(self, arg):
        """Creates a new instance of a specified class, saves it to the JSON file, and prints its ID."""
        if not arg:
            print("** class name missing **")
            return

        class_name = arg.strip()
        if class_name not in self.class_dict:
            print("** class doesn't exist **")
            return

        obj = self.class_dict[class_name]()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and ID."""
        args = arg.split()
        if len(args) < 2:
            print("** class name and instance id are required **")
            return

        class_name, instance_id = args
        obj_dict = storage.all()
        key = f"{class_name}.{instance_id}"

        if key in obj_dict:
            print(obj_dict[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and ID."""
        args = arg.split()
        if len(args) < 2:
            print("** class name and instance id are required **")
            return

        class_name, instance_id = args
        obj_dict = storage.all()
        key = f"{class_name}.{instance_id}"

        if key in obj_dict:
            del obj_dict[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints string representations of all instances or all instances of a specific class."""
        obj_dict = storage.all()
        if arg:
            if arg in self.class_dict:
                print([str(obj) for obj in self.class_dict[arg].all()])
            else:
                print("** class doesn't exist **")
        else:
            print([str(obj) for obj in obj_dict.values()])

    def do_update(self, arg):
        """Updates an instance based on the class name and ID with a dictionary."""
        args = arg.split()
        if len(args) < 3:
            print("** class name, instance id, and dictionary representation are required **")
            return

        class_name, instance_id, json_dict = args[0], args[1], ' '.join(args[2:])
        obj_dict = storage.all()
        key = f"{class_name}.{instance_id}"

        if key in obj_dict:
            obj = obj_dict[key]
            try:
                # Use json.loads to parse the dictionary representation
                update_dict = json.loads(json_dict.replace("'", "\""))
                for attr, value in update_dict.items():
                    # Use proper type conversion based on the attribute type
                    setattr(obj, attr, type(getattr(obj, attr))(value))
                obj.save()
            except ValueError:
                print("** invalid dictionary representation **")
        else:
            print("** no instance found **")

    def do_count(self, arg):
        """Counts the number of instances of a class."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0].strip()
        if class_name not in self.class_dict:
            print("** class doesn't exist **")
            return

        count = len([obj for obj in storage.all().values() if isinstance(obj, self.class_dict[class_name])])
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
