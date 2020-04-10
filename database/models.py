from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Document):
    fname = db.StringField(required=False, unique=False)
    lname = db.StringField(required=False, unique=False)
    timestamp = db.StringField(required=True, unique=False)
    uuid = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)