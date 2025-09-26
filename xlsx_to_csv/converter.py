import os
import sys
import pandas as pd
import requests
import re

# Checking if the input is a Google Sheets link
def is_google_sheets_link(input_str):
    return "docs.google.com/spreadsheets" in input_str

# Extracting the sheet ID from the Google Sheets URL
def extract_sheet_id(url):
    # Extract Google Sheet ID from URL
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
    return match.group(1) if match else None

# Downloading the Google Sheet as an Excel file
def download_google_sheet(sheet_url, output_file):
    sheet_id = extract_sheet_id(sheet_url)
    if not sheet_id:
        print("❌ Could not extract Sheet ID from the link.")
        return None

    # Constructing the export URL
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    print(f"Downloading Google Sheet from: {export_url}")
    response = requests.get(export_url)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {output_file}")
        return output_file
    else:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")
        return None

# Converting the downloaded or local Excel file to CSV files
def convert_xlsx_to_csv(input_path):
    # Creating output directory based on the input file name
    base_name = os.path.basename(input_path)
    if base_name.endswith(".xlsx"):
        base_name = base_name[:-5]

    output_dir = f"csv_files/{base_name}"
    os.makedirs(output_dir, exist_ok=True)

    try:
        excel_data = pd.read_excel(input_path, sheet_name=None, engine='openpyxl')
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    # Saving each sheet as a separate CSV file
    for sheet_name, df in excel_data.items():
        output_file = os.path.join(output_dir, f"{sheet_name}.csv")
        try:
            df.to_csv(output_file, index=False)
            print(f"Saved: {output_file}")
        except Exception as e:
            print(f"Failed to save '{sheet_name}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input should be:\n  python converter.py <google_sheet_link | local_xlsx_file>")
        sys.exit(1)

    input_arg = sys.argv[1]

    # Determine if input is a Google Sheets link or a local file path
    if is_google_sheets_link(input_arg):
        downloaded_file = "xlsx_files/downloaded_sheet.xlsx"
        result_file = download_google_sheet(input_arg, downloaded_file)
        if result_file:
            convert_xlsx_to_csv(result_file)
    else:
        if not os.path.exists(input_arg):
            print(f"File not found: {input_arg}")
        else:
            convert_xlsx_to_csv(input_arg)

