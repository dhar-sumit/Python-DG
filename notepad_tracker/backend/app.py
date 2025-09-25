# backend/app.py
from flask import Flask
from backend.routes import main as main_routes

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.register_blueprint(main_routes)
    return app
