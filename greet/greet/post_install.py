import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.py")

def configure_env_path():
    """Prompt the user for a .env file path and update config.py"""
    env_path = input("Enter the absolute path to your .env file (default: ~/.greet_env): ").strip()
    if not env_path:
        env_path = os.path.expanduser("~/.greet_env")  # Default location

    # Modify config.py to use the provided path
    with open(CONFIG_FILE, "w") as f:
        f.write(f"""import os
from dotenv import load_dotenv

# Load environment variables from the user-provided path
ENV_PATH = r"{env_path}"
load_dotenv(ENV_PATH)

# Access the environment variable
name = os.getenv('NAME', 'World')  # Default to "World" if NAME is not set
""")

    print(f".env path set to: {env_path}")

if __name__ == "__main__":
    configure_env_path()
