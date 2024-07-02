#!/usr/bin/python3
""" holds class Appointment"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Appointment(BaseModel, Base):
    """Representation of an Appointment"""
    if models.type_of_storage == 'db':
        __tablename__ = 'appointments'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
        doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
        email = Column(String(255), nullable=False)
        patient_name = Column(String(255), nullable=False)
        date = Column(String(255), nullable=False)
        time = Column(String(255), nullable=False)
        status = Column(String(255), default='pending')

    else:
        user_id = ""
        doctor_id = ""
        email = ""
        pateint_name = ""
        date = ""
        time = ""
        status = ""


    def __init__(self, *args, **kwargs):
        """initializes Appointment"""
        super().__init__(*args, **kwargs)
