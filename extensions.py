from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import settings
from src.controllers.auth import auth_bp
from src.controllers.user import user_bp
from data.models import WPTokenBlocList
import extensions

app = Flask(__name__)
# app.config.from_prefixed_env()

app.config.from_object(settings)

# add blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

jwt = JWTManager(app)

# additional claims (add claim to token)
# @jwt.additional_claims_loader
# def make_additional_claims(identity):
#     if identity == "":
#         return {"is_staff": True}
#     return {"is_staff": False}

# jwt error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify(
        {
            "message": "Token has expired",
            "error": "token_expired"
        }
    ), 401

@jwt.expired_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            "message": "Siggnature verification failed",
            "error": "invalid_token"
        }
    ), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {
            "message": "Request doesnt contain valid token",
            "error": "authorization_header"
        }
    ), 401


@jwt.token_in_blocklist_loader
def token_in_bloclist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']

    token = WPTokenBlocList.get_jti(jti).scalar()

    return token is not None

if __name__ == "__main__":
    app.run(debug=True, port=9098, host="localhost")


# if hasattr(jack, "addresses"):