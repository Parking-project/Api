"""Flask config class."""
import os
from .base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False