from config import configurations
from flask import Flask

def register_config(app: Flask):
    app.config.from_object(configurations)
