# services/postalZip_format.py

import pandas as pd
import re

def clean_postal_zip(df: pd.DataFrame, column: str = "postalZip") -> pd.DataFrame:
    """
    Convert all postalZip values to integers.
    Remove letters, keep only numbers.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    def to_int(val):
        # Convert to string, remove non-digit characters
        s = str(val)
        digits = re.findall(r'\d+', s)
        if digits:
            return int("".join(digits))
        else:
            return 0 
    
    df[column] = df[column].apply(to_int)
    return df
