import os
import json

def load_config(config_path='config/config.json', handle_failure=True, config_data={}):
    """Load configuration from a JSON file."""
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        if handle_failure:
            with open(config_path, 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            print("Configuration file created with default settings.")
            return config_data
            
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        print("Configuration file loaded successfully.")
    return config