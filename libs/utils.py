import os
import json
import logging

logger = logging.getLogger(__name__)

def load_config(config_path='config/config.json', handle_failure=True, config_data={}):
    """Load configuration from a JSON file."""
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        if handle_failure:
            with open(config_path, 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            logger.info("Configuration file created with default settings.")
            return config_data

        logger.error(f"Configuration file not found: {config_path}")            
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        logger.info(f"Configuration loaded from {config_path}")
    return config