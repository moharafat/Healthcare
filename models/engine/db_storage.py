#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.doctor import Doctor
from models.base_model import BaseModel, Base
from models.schedule import DoctorSchedule
from models.prescription import Prescription
from models.appointment import Appointment
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Doctor": Doctor, "DoctorSchedule": DoctorSchedule,
           "Prescription": Prescription, "Appointment": Appointment, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HC_USER = getenv('HC_USER')
        HC_PWD = getenv('HC_PWD')
        HC_HOST = getenv('HC_HOST')
        HC_DB = getenv('HC_DB')
        HC_ENV = getenv('HC_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HC_USER,
                                             HC_PWD,
                                             HC_HOST,
                                             HC_DB))
        if HC_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def get_doctor_id(self, cls, doctor_name):
        """
        Returns the the doctor's id based on his/her first and last name
        """
        if cls not in classes.values():
            return None
        doc_name = str(doctor_name)
        first_name, last_name = doc_name.split()
        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.first_name == first_name) and (value.last_name == last_name):
                return value.id
        return None


    def get_user_id(self, cls, email):
        """
        Returns the the user's id based on his/her email
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.email == email):
                return value.id

        return None

    def get_doctors(self, cls, speciality):
        """
        Returns a list of doctor objects based on the provided speciality
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        doctors_list = []
        for value in all_cls.values():
            if (value.specialty == speciality):
                doctors_list.append(value)

        return doctors_list
