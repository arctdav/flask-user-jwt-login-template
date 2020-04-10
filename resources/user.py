"""
This is the user module and supports all the ReST actions for the
USER collection
"""
# UUID Library
import uuid

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from flask_jwt_extended import jwt_required

# database schema
from database.models import User



def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all():
    """
    This function responds to a request for /api/blog-user
    with the complete lists of user
    :return: list of user in json
    """
    user = User.objects()
    return user


def read_one(user_uuid):
    """
    This function responds to a request for /api/blog-user/{uuid}
    with one matching user from user
    :param user_uuid:   uuid of user to find
    :return:        user matching 
    """
    # MongoEngine database query
    USER = User.objects(uuid__not__ne=user_uuid)
    # Does the user exist in user?
    if USER:
        return USER[0]

    # otherwise, nope, not found
    else:
        abort(
            404, "User with uuid {uuid} not found".format(uuid=user_uuid)
        )

@jwt_required
def update(user_uuid, update_user):
    """
    This function updates an existing user in the user structure
    :param user_uuid:   uuid of user to update in the user structure
    :param user:  user to update
    :return:        updated user structure
    """
    USER = User.objects(uuid__not__ne=user_uuid)
    if USER:
        USER[0].update(fname=update_user['fname'],
                         lname=update_user['lname'], timestamp=get_timestamp())
        return make_response(
            "{uuid} successfully updated".format(uuid=user_uuid), 204
        )
    else:
        abort(
            404, "User with uuid {uuid} not found".format(uuid=user_uuid)
        )

@jwt_required
def delete(user_uuid):
    """
    This function deletes a user from the user structure
    :param user_uuid:   uuid of user to delete
    :return:        200 on successful delete, 404 if not found
    """
    USER = User.objects(uuid__not__ne=user_uuid)

    # Does the user to delete exist?
    if USER:
        USER[0].delete()
        return make_response(
            "User with uuid {uuid} successfully deleted".format(
                uuid=user_uuid), 200
        )

    # Otherwise, nope, user to delete not found
    else:
        abort(
            404, "User with uuid {uuid} not found".format(uuid=user_uuid)
        )
