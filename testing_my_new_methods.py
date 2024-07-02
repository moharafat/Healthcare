#!/usr/bin/python3
""" Testing
"""
from models import storage
from models.doctor import Doctor
from models.user import User

doc_name = "Khaled Gad"
doctor_id = storage.get_doctor_id(Doctor, doc_name)
if doctor_id is None:
    print("Doctor not found")
else:
    print(doctor_id)
email = "Rahafmohamed545@gmail.com"
print("user_id: {}".format(storage.get_user_id(User, email)))
iddd = "41198644-7f6d-4911-8ca2-2edf459ec4f2"
instance = storage.get(Doctor, iddd)
print(instance.first_name)
