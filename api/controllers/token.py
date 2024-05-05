from flask import Blueprint, jsonify, request
from core.domain.entity import WPRole, WPUser, WPUserMeta, WPTokenBlocList, WPAuthHistory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from api.shared.global_exception import *
from api.validators import NoneValidator, DataExistValidator, IsInt, IsStr, UserValidator
from datetime import timedelta

blueprint = Blueprint('token', __name__, url_prefix="/token")

def sign_in(user_id: str):
    WPAuthHistory(user_id=user_id).save()

@blueprint.post('/login')
def login():
    data = request.get_json()
    DataExistValidator(
        {
            "login": IsStr(),
            "password": IsStr(),
        }
    ).validate_exist(**data)
    user: WPUser = NoneValidator.validate(key="user object", value=WPUser.authenticate(**data))
    tokens = user.get_tokens()
    sign_in(user.ID)
    return jsonify(
        {
            "message": "Авторизация прошла успешно",
            "tokens": tokens,
            "role": WPRole.get_id(user.role_id).role_name
        }
    )

@blueprint.post('/register')
def register():
    data = request.get_json()
    DataExistValidator(
        {
            "login": IsStr(),
            "password": IsStr(),
            "display_name": IsStr()
        }
    ).validate_exist(**data)
    UserValidator.validate(data.get("login"), data.get("password"), data.get("display_name"))
    UserValidator.validate_unique(data.get("login"))
        
    user = WPUser(**data)
    user.save()
    tokens = user.get_tokens()
    sign_in(user.ID)
    return jsonify(
        {
            "message": "Регистрация прошла успешно",
            "tokens": tokens
        }
    ), 200

@blueprint.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity, expires_delta=timedelta(24))
    return jsonify(
        {
            "access": new_access_token
        }
    )

@blueprint.get('/logout')
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']
    NoneValidator.validate(
        key="user_telegram id",
        value=WPUserMeta.get_user_id(user_id=jwt["sub"]["user_id"])
    ).delete()
    token_b = WPTokenBlocList(jti=jti)

    token_b.save()

    return jsonify(
        {
            "message": f"{token_type} token revoked successfully"
        }
    ), 200


@blueprint.get('/check')
@jwt_required()
def check():
    return jsonify(
        {
            "message": "OK"
        }
    )