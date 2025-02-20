import os
from dotenv import load_dotenv

# Load environment variables from the user-provided path
ENV_PATH = r"C:\Users\boria/.greet_env"
load_dotenv(ENV_PATH)

# Access the environment variable
name = os.getenv('NAME', 'World')  # Default to "World" if NAME is not set
