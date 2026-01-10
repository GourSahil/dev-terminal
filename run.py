from app.dev_terminal import App
from libs.utils import load_config
import os

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json') # configuration path basically config/config.json, using os to make it cross platform
# loading the configuration
config = load_config(
    config_path=config_path, 
    handle_failure=True, 
    config_data={"host": "127.0.0.1", "port": 5000, "debug": False} # backup default config
        )

# configuation for flask app folders
flask_config = {
    "templates_folder": os.path.join(os.path.dirname(__file__), 'templates'),
    "static_folder": os.path.join(os.path.dirname(__file__), 'static')
}

if __name__ == "__main__":
    app_instance = App(
        template_folder=flask_config["templates_folder"],
        static_folder=flask_config["static_folder"]
    )
    app = app_instance.get_app()
    app.run(
        host=config["host"],
        port=config["port"],
        debug=config.get("debug", False)
    )