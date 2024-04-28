"""Flask config class."""
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    CON_STRING: str = os.getenv('CON_STRING')
    USER: str = os.getenv('USER')
    PASS: str = os.getenv('PASS')