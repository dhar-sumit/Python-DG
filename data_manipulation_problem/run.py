# run.py

from db.loader import load_json_to_db
from db.fetcher import fetch_table_as_df

from services.email_format import format_email
from services.postalZip_format import clean_postal_zip
from services.phone_format import format_phone_number

def main():
    json_file = "data/sample_data_for_assignment.json"
    
    # Step 1: Load into SQLite
    load_json_to_db(json_file)
    
    # Step 2: Fetch back as pandas DataFrame
    table_name = "json_to_sql_table"
    df = fetch_table_as_df(table_name)
    print("\nDataFrame from DB before formatting:")
    print(df.head())  # shows first 5 rows

    df = format_email(df)
    df = clean_postal_zip(df)
    df = format_phone_number(df)

    print("\nDataFrame from DB after formatting:")
    print(df.head())  # shows first 5 rows

if __name__ == "__main__":
    main()
