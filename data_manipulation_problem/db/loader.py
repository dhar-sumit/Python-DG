# database/loader.py
# loads JSON into SQLite database using SQLAlchemy

import pandas as pd
import json
from db.connection import get_engine

def load_json_to_db(json_path: str, table_name: str = "json_to_sql_table"):
    engine = get_engine()

    # Load raw JSON
    with open(json_path, "r") as f:
        raw = json.load(f)
    
    # Build DataFrame
    df = pd.DataFrame(raw["data"], columns=raw["cols"])
    
    # Save to SQLite
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Data loaded into table: {table_name}")
