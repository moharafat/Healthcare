#!/usr/bin/python3
""" objects that handle all default RestFul API actions for users """
from models.user import User
from models.doctor import Doctor
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates either a patent or a doctor object based on the role provided
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    role = data.pop('role')
    if role == 'user':
        if 'email' not in request.get_json():
            abort(400, description="Missing email")
        if 'first_name' not in request.get_json():
            abort(400, description="Missing first_name")
        if 'last_name' not in request.get_json():
            abort(400, description="Missing last_name")
        instance = User(**data)
    elif role == 'doctor':
        if 'email' not in request.get_json():
            abort(400, description="Missing email")
        if 'first_name' not in request.get_json():
            abort(400, description="Missing first_name")
        if 'last_name' not in request.get_json():
            abort(400, description="Missing last_name")
        if 'specialty' not in request.get_json():
            abort(400, description="Missing specialty")
        instance = Doctor(**data)
    else:
        abort(400, description="Missing role")
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a user obj """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user Object
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a user object
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
