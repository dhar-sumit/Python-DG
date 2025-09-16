# Write a program anti_html.py that takes a URL as an argument, downloads the HTML from the web, and prints it after stripping HTML tags.

# To achieve this we can use requests, beautifulsoup to extract contents.

import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str):
    try:
        # fetching the page response
        response = requests.get(url)

        # raising  error for bad requests/status
        response.raise_for_status()  

        # parsing the  HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # extracting text and removing HTML tags
        text = soup.get_text(separator="\n", strip=True)

        return text

    except Exception as e:
        print(f"Error: {e}")
        return None

url = 'https://datagrokr.co'
content = extract_text_from_url(url)

print(f'Text extracted from given url: "{url}"\n\n {content}')
