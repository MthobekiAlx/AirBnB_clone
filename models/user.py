from models.base_model import BaseModel

class User(BaseModel):
    """
    User class: Inherits from BaseModel and represents a user.
    """
    email = ""        # User's email address
    password = ""     # User's password
    first_name = ""    # User's first name
    last_name = ""     # User's last name
