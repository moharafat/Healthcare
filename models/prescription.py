#!/usr/bin/python3
""" holds class Prescription"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Prescription(BaseModel, Base):
    """Representation of a Prescription"""
    if models.type_of_storage == 'db':
        __tablename__ = 'prescriptions'
        appointment_id = Column(String(60), ForeignKey('appointments.id'), nullable=False)
        doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
        patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
        medication = Column(String(255), nullable=False)
        dosage = Column(String(255), nullable=False)
        instructions = Column(String(1024), nullable=True)
        appointment = relationship("Appointment", backref="prescriptions")
    else:
        appointment_id = ""
        doctor_id = ""
        patient_id = ""
        dosage = ""
        instructions = ""

    def __init__(self, *args, **kwargs):
        """initializes Prescription"""
        super().__init__(*args, **kwargs)
