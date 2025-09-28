# database/fetcher.py
# fetches table → pandas, from SQLite database using SQLAlchemy

import pandas as pd
from db.connection import get_engine

def fetch_table_as_df(table_name: str = "json_to_sql_table") -> pd.DataFrame:
    engine = get_engine()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df
