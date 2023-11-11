# models/amenity.py
from models.base_model import BaseModel

class Amenity(BaseModel):
    name = ""
    description = ""

    def __init__(self, *args, **kwargs):
        """Initialize Amenity with more attributes"""
        self.description = kwargs.get('description', "")
        super().__init__(*args, **kwargs)
