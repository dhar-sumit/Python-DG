# backend/routes.py
from flask import Blueprint, request, jsonify, render_template
from backend.utils.file_utils import save_file
from backend.utils.git_utils import commit_file
import os
from backend.config import DEFAULT_SAVE_DIR

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('index.html')

@main.route('/check_path', methods=['POST'])
def check_path():
    data = request.get_json()
    path = data.get('path', '').strip()

    if not path:
        return jsonify({"status": "error", "message": "Path is required"}), 400

    if os.path.isfile(path):
        return jsonify({"status": "file"})
    elif os.path.isdir(path):
        return jsonify({"status": "directory"})
    else:
        return jsonify({"status": "not_exist"})

@main.route('/load', methods=['POST'])
def load_file():
    data = request.get_json()
    filepath = data.get('filepath')

    if not filepath or not filepath.strip():
        return jsonify({"status": "error", "message": "File path is required"}), 400

    if not os.path.isfile(filepath):
        return jsonify({"status": "error", "message": "File does not exist"}), 404

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"status": "success", "content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@main.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    content = data.get('content', '')
    filepath = data.get('filepath')

    if not filepath:
        return jsonify({"status": "error", "message": "Filepath is required"}), 400
    
    # If filepath is directory, append default filename
    if os.path.isdir(filepath):
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'notes_{timestamp}.txt'
        filepath = os.path.join(filepath, filename)

    save_file(filepath, content)
    commit_file(filepath)

    return jsonify({"status": "success", "filepath": filepath})
