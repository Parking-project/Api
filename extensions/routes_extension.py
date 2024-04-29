from flask import Flask
from apps.api.controllers.auth_controller import blueprint as auth_bp

def register_routes(app: Flask):
    """
    Register routes with blueprint and namespace
    """
    app.register_blueprint(auth_bp)
    pass