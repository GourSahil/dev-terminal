import os
from dotenv import load_dotenv
from pathlib import Path

# Loading environment variables from .env file
BASE_DIR = Path(__file__).resolve().parents[0]
env_path = BASE_DIR / "config" / ".env"
load_dotenv(dotenv_path=env_path)

from libs.logger import setup_logging
from app.dev_terminal import App
from libs.utils import load_config

# defining paths
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json') # configuration path basically config/config.json, using os to make it cross platform
log_file_path = Path("logs") / "app.log"

# Setting up logging
os.makedirs("logs", exist_ok=True)
setup_logging(log_file_path, debug=True)

# loading the configuration
config = load_config(
    config_path=config_path, 
    handle_failure=True, 
    config_data={"host": "127.0.0.1", "port": 5000, "debug": False} # backup default config
        )

import logging
logger = logging.getLogger(__name__)

# configuation for flask app folders
flask_config = {
    "templates_folder": os.path.join(os.path.dirname(__file__), 'templates'),
    "static_folder": os.path.join(os.path.dirname(__file__), 'static')
}

if __name__ == "__main__":
    logger.info("Starting the Dev Terminal application...")
    app_instance = App(
        template_folder=flask_config["templates_folder"],
        static_folder=flask_config["static_folder"],
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY")
    )
    
    app = app_instance.get_app()
    app.run(
        host=config["host"],
        port=config["port"],
        debug=config.get("debug", False),
        use_reloader=config.get("use_reloader", False)
    )