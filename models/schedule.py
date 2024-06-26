#!/usr/bin/python3
""" holds class DoctorSchedule"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class DoctorSchedule(BaseModel, Base):
    """Representation of a Doctor's Schedule"""
    if models.type_of_storage == 'db':
        __tablename__ = 'doctor_schedules'
        doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
        day_of_week = Column(String(255), nullable=False)
        start_time = Column(String(255), nullable=False)
        end_time = Column(String(255), nullable=False)
    else:
        doctor_id = ""
        day_of_week = ""
        start_time = ""
        end_time = ""

    def __init__(self, *args, **kwargs):
        """initializes DoctorSchedule"""
        super().__init__(*args, **kwargs)
