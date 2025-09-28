# database/connection.py
# creates SQLAlchemy engine for SQLite database

import os
from sqlalchemy import create_engine

DB_NAME = "json_to_sql.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_engine():
    return create_engine("sqlite:///" + DB_PATH, echo=False)
