"""Flask config class."""
import os
from .base_config import BaseConfig


class ProductionConfig(BaseConfig, DatabaseConfig):
    DEBUG = False
    TESTING = False