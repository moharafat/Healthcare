#!/usr/bin/python3
""" objects that handle all default RestFul API actions for doctors """
from models.doctor import Doctor
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/filter_doctors', methods=['GET'], strict_slashes=False)
def filter_doctors():
    """
    Retrieves the list of all doctors objects based on the provided speciality
    """
    doctor_speciality = request.args.get("specialty")
    if not doctor_speciality:
        abort(400, description="doctor specialty parameter is required")

    doctors_list =storage.get_doctors(Doctor, doctor_speciality)
    doctors_dict = [doctor.to_dict() for doctor in doctors_list]

    return jsonify(doctors_dict)


@app_views.route('/doctors', methods=['GET'], strict_slashes=False)
def get_doctors():
    """
    Retrieves the list of all doctors objects
    """
    all_doctors = storage.all(Doctor).values()
    list_doctors = []
    for doctor in all_doctors:
        list_doctors.append(doctor.to_dict())
    return jsonify(list_doctors)


@app_views.route('/doctors/<doctor_id>', methods=['GET'], strict_slashes=False)
def get_doctor(doctor_id):
    """ Retrieves a doctor """
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)

    return jsonify(doctor.to_dict())


@app_views.route('/doctors/<doctor_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_doctor(doctor_id):
    """
    Deletes a doctor Object
    """
    doctor = storage.get(Doctor, doctor_id)

    if not doctor:
        abort(404)

    storage.delete(doctor)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/doctors/<doctor_id>', methods=['PUT'], strict_slashes=False)
def put_doctor(doctor_id):
    """
    Updates a doctor object
    """
    doctor = storage.get(Doctor, doctor_id)

    if not doctor:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(doctor, key, value)
    storage.save()
    return make_response(jsonify(doctor.to_dict()), 200)
