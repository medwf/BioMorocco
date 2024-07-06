#!/usr/bin/python3
"""
initialize the models package
"""

from models.engine.DBstorage import DBStorage


storage = DBStorage()
storage.reload()
