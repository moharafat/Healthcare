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
        patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
        doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
        date = Column(String(255), nullable=False)
        time = Column(String(255), nullable=False)
        status = Column(String(255), nullable=False)

    else:
        patient_id = ""
        doctor_id = ""
        date = ""
        time = ""
        status = ""


    def __init__(self, *args, **kwargs):
        """initializes Appointment"""
        super().__init__(*args, **kwargs)
