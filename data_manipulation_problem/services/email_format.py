# services/email_format.py

import pandas as pd

def format_email(df: pd.DataFrame, column: str = "email") -> pd.DataFrame:
    """
    Convert all emails to format: username@gmail.com
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    df[column] = df[column].apply(lambda x: f"{str(x).split('@')[0]}@gmail.com")
    return df
