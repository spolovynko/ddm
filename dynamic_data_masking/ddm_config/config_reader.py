import os
import sys
from dotenv import load_dotenv

class ConfigReader:
    _instance = None

    def __new__(cls, env_path=None):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._load_env(env_path)
        return cls._instance

    def _load_env(self, env_path='C:\WORK\ddm_api\ddm\.env'):
        default_paths = [
            env_path,  # User-defined path (if provided)
            os.path.join(os.getcwd(), ".env"),  # Current working directory
            os.path.join(os.path.dirname(__file__), "..", ".env"),  # Package root
            os.path.expanduser("~/.ddm_env"),  # User home directory
            "/etc/ddm/.env",  # System-wide configuration (Linux/macOS)
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),  # Module directory
            os.path.join(sys.prefix, ".env"),  # Virtual environment (if applicable)
        ]

        for path in default_paths:
            if path and os.path.exists(path):
                load_dotenv(path)
                return
    def get(self, key, default=None):
        value = os.getenv(key, default)
        if value is None:
            print(f"⚠️ Warning: {key} not found in environment variables.")
        return value

# Initialize ConfigReader (Automatically finds .env)
config = ConfigReader()
