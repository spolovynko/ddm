import os
from dotenv import load_dotenv

class ConfigReader:
    _instance = None

    def __new__(cls, env_path=".env"):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._load_env(env_path)
        return cls._instance

    def _load_env(self, env_path):
        load_dotenv(env_path)

    def get(self, key, default=None):
        return os.getenv(key, default)

config = ConfigReader()
