# backend/utils/file_utils.py
import os

def save_file(filepath, content):
    dir_path = os.path.dirname(filepath)
    os.makedirs(dir_path, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
