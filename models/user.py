#!/usr/bin/python3
""" holds class user"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.type_of_storage == 'db':
        __tablename__ = 'users'
        email = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        appointments = relationship("Appointment", backref="user")
        prescriptions = relationship("Prescription", backref="user")
    else:
        email = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
