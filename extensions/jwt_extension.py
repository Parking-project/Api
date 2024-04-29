from flask import jsonify
from flask_jwt_extended import JWTManager
from core.domain.entity.WPTokenBlocList import WPTokenBlocList

def register_jwt(jwt: JWTManager):
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
