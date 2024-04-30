from flask import Flask
from apps.api.controllers.auth import blueprint as auth_bp
from apps.api.controllers.document import blueprint as document_bp
from apps.api.controllers.message import blueprint as message_bp
from apps.api.controllers.place import blueprint as place_bp
from apps.api.controllers.reserve_history import blueprint as reserve_history_bp
from apps.api.controllers.reserve import blueprint as reserve_bp
from apps.api.controllers.role import blueprint as role_bp
from apps.api.controllers.token_bloc_list import blueprint as token_bloc_list_bp
from apps.api.controllers.token import blueprint as token_bp
from apps.api.controllers.user import blueprint as user_bp

def register_routes(app: Flask):
    """
    Register routes with blueprint and namespace
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(place_bp)
    app.register_blueprint(reserve_history_bp)
    app.register_blueprint(reserve_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(token_bloc_list_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(user_bp)
    pass