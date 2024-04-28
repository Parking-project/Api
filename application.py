from flask import Flask
from flask_jwt_extended import JWTManager

from extensions.routes_extension import register_routes
from extensions.exception_extension import register_exception_handler

def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)
    
    register_routes(app)
    register_exception_handler(app)
    return app, jwt