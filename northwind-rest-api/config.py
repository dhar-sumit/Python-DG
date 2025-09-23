# config.py
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
BASE_DIR = os.path.dirname(__file__)

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'northwind.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
