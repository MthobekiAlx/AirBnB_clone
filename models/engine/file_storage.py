# models/engine/file_storage.py
import json

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        obj_dict = {obj.id: obj.to_dict() for obj in FileStorage.__objects.values()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objs = json.load(f)
                for obj_id, obj_data in objs.items():
                    cls_name = obj_data['__class__']
                    cls = globals()[cls_name]
                    obj = cls(**obj_data)
                    FileStorage.__objects[obj_id] = obj
        except FileNotFoundError:
            pass
