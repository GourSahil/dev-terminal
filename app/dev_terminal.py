from flask import Flask
from pathlib import Path
import logging
import os

# importing the blueprints
from app.routes.index import index_bp
from libs.supabase_client import create_client

logger = logging.getLogger(__name__)

class App:
    """
    Main application class to initialize the Flask app and register blueprints.
    """
    def __init__(self, template_folder: str = "templates", static_folder: str = "static", supabase_url: str = None, supabase_key: str = None):
        if (supabase_url is None) or (supabase_key is None):
            logger.error("Supabase URL or Key not provided.")
            raise ValueError("Supabase URL and Key must be provided to create the client.")
        
        self.flask_app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        self.flask_app.supabase = create_client(supabase_url=supabase_url, supabase_key=supabase_key)

        # registering the blueprints here
        self.flask_app.register_blueprint(index_bp)

    def get_app(self) -> Flask:
        return self.flask_app