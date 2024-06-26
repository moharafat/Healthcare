#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


type_of_storage = getenv("HC_STORAGE")

if type_of_storage == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
