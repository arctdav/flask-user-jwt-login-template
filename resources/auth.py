# UUID Library
import uuid

# System modules
# from datetime import datetime
import datetime
import re 

# 3rd party modules
from flask import make_response, abort
from flask_jwt_extended import create_access_token

# Database
from database.models import User
  

def isEmail(email):
    if email == None: return False
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True  
    else:  
        return False

def get_timestamp():
    return datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def get_uuid():
    return str(uuid.uuid1())

def signup(user):
    email = user.get("email", None)
    if not isEmail(email):
        abort(
            404, "User email {email} is not valid".format(
                email=email),
        )
    USER = User.objects(email__not__ne=email)

    if USER:
        abort(
            404, "User with email {email} already exists".format(
                email=email),
        )

    user_uuid = get_uuid()
    newUser = User(**user)
    newUser.timestamp = get_timestamp()
    newUser.uuid = user_uuid
    newUser.hash_password()
    newUser.save()
    return make_response(
        "{uuid} successfully created".format(uuid=user_uuid), 200
    )

def login(loginUser):
    user = User.objects().get(email=loginUser.get('email'))
    if not user:
        abort(
            404, "User with email {email} does not exists".format(
                email=loginUser.get('email')),
        )
    print(dir(user))
    authorized = user.check_password(loginUser.get('password'))
    if not authorized:
        abort(
            404, "User with email {email} password incorrect".format(
                email=loginUser.get('email')),
        )
    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=str(user.uuid), expires_delta=expires)
    return {'token': access_token}, 200