#!/usr/bin/python3
""" holds class Patient"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Patient(BaseModel, Base):
    """Representation of a Patient """
    if models.type_of_storage == 'db':
        __tablename__ = 'patients'
        email = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        appointments = relationship("Appointment", backref="patient")
        prescriptions = relationship("Prescription", backref="patient")
    else:
        email = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes Patient"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
