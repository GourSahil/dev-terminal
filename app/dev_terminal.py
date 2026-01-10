from flask import Flask

# importing the blueprints
from app.routes.index import index_bp

class App:
    """
    Main application class to initialize the Flask app and register blueprints.
    """
    def __init__(self, template_folder: str = "templates", static_folder: str = "static"):
        self.flask_app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

        # registering the blueprints here
        self.flask_app.register_blueprint(index_bp)

    def get_app(self) -> Flask:
        return self.flask_app