"""Flask config class."""
import os


class DatabaseConfig:
    CON_STRING: str = os.getenv('CON_STRING')
    USER: str = os.getenv('USER')
    PASS: str = os.getenv('PASS')