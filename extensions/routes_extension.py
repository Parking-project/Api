from flask import Flask, request, Response
from flask_cors import CORS
from api.controllers import (
    auth_bp,
    document_bp,
    message_bp,
    place_bp,
    reserve_history_bp,
    reserve_bp,
    role_bp,
    token_bloc_list_bp,
    token_bp,
    user_bp
)

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
    CORS(app)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = Response()
            res.headers['X-Content-Type-Options'] = '*'
            return res
    pass