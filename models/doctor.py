#!/usr/bin/python3
""" holds class Doctor"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Doctor(BaseModel, Base):
    """Representation of a Doctor """
    if models.type_of_storage == 'db':
        __tablename__ = 'doctors'
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        email = Column(String(255), nullable=False)
        specialty = Column(String(255), nullable=False)
        location = Column(String(255), nullable=True)
        appointments = relationship("Appointment", backref="doctor")
        prescriptions = relationship("Prescription", backref="doctor")
        schedules = relationship("DoctorSchedule", backref="doctor")
    else:
        first_name = ""
        last_name = ""
        email = ""
        specialty = ""
        location = ""

    def __init__(self, *args, **kwargs):
        """initializes Doctor"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption if attribute is password"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
