#!/usr/bin/python3
""" objects that handle all default RestFul API actions for appointments """
from models.user import User
from models.doctor import Doctor
from models.appointment import Appointment
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import sys


@app_views.route('/appointments', methods=['POST'], strict_slashes=False)
def post_appointment():
    """
    Creates either an appointment object based on the args provided
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'patient_name' not in request.get_json():
        abort(400, description="Missing patient name")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'doctor_name' not in request.get_json():
        abort(400, description="Missing doctor name")
    if 'date' not in request.get_json():
        abort(400, description="Missing date")
    if 'time' not in request.get_json():
        abort(400, description="Missing time")

    data = request.get_json()
    doctor_name = data.pop('doctor_name')
    doctor_id = storage.get_doctor_id(Doctor, doctor_name)
    if doctor_id is None:
        abort(400, description="Doctor not found")
    else:
        data['doctor_id'] = doctor_id
    email = data.get('email')
    user_id = storage.get_user_id(User, email)
    if user_id:
        data['user_id'] = user_id
    instance = Appointment(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/appointments/<appointment_id>', methods=['PUT'], strict_slashes=False)
def put_appointment(appointment_id):
    """
    Updates an appointment object
    """
    appointment = storage.get(Appointment, appointment_id)

    if not appointment:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    if 'doctor_name' in request.get_json():
        doc_name = data.pop('doctor_name')
        doctor_id = storage.get_doctor_id(Doctor, doc_name)
        if not doctor_id:
            abort(400, description="Doctor not found")
        data['doctor_id'] = doctor_id
    if 'email' in request.get_json():
        email = data.get('email')
        user_id = storage.get_user_id(User, email)
        if user_id:
            data['user_id'] = user_id
        else:
            data['user_id'] = None
    for key, value in data.items():
        if key not in ignore:
            setattr(appointment, key, value)
    storage.save()
    return make_response(jsonify(appointment.to_dict()), 200)

@app_views.route('/appointments/<appointment_id>', methods=['GET'], strict_slashes=False)
def get_appointment(appointment_id):
    """ Retrieves an appointment obj """
    appointment = storage.get(Appointment, appointment_id)
    if not appointment:
        abort(404)

    return jsonify(appointment.to_dict())


@app_views.route('/appointments/<appointment_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_appointment(appointment_id):
    """
    Deletes an appointment Object
    """
    appointment = storage.get(Appointment, appointment_id)

    if not appointment:
        abort(404)

    storage.delete(appointment)
    storage.save()

    return make_response(jsonify({}), 200)
