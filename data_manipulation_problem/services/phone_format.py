# services/phone_format.py

import pandas as pd
import re

def format_phone_number(df: pd.DataFrame, column: str = "phone") -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    def phone_number_to_ascii(phone):
        # Remove non-digit chars
        digits = re.sub(r'\D', '', str(phone))
        result = ""
        for i in range(0, len(digits) - 1, 2):  # take 2 digits at a time
            num = int(digits[i:i+2])
            if 65 <= num <= 99:
                result += chr(num)
            else:
                result += "O"
        return result
    
    new_column = "coded_phone_number"
    df[new_column] = df[column].apply(phone_number_to_ascii)
    df.drop(columns=[column], inplace=True)
    return df