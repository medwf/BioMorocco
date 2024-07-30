#!/usr/bin/python3
"""
initialize the models package
"""

from models.engine.DBstorage import DBStorage
from dotenv import load_dotenv
load_dotenv()

storage = DBStorage()
storage.reload()
