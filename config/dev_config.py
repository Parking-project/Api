"""Flask config class."""
import os
from .base_config import BaseConfig
from .database_config import DatabaseConfig


class ProductionConfig(BaseConfig, DatabaseConfig):
    DEBUG = True
    TESTING = False