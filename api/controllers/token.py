from flask import Blueprint, jsonify, request
from core.domain.entity import WPRole, WPUser, WPUserMeta, WPTokenBlocList, WPAuthHistory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from api.shared.global_exception import *
from api.validators import NoneValidator, DataExistValidator, IsInt, IsStr, UserValidator, JwtValidator
from datetime import timedelta

blueprint = Blueprint('token', __name__, url_prefix="/token")

def sign_in(user_id: str, user_name: str):
    WPAuthHistory(
        user_id=user_id,
        user_name=user_name
    ).save()

def log_out(jwt: dict):
    jti = jwt['jti']
    user_meta: WPUserMeta = WPUserMeta.get_user_id(user_id=jwt["sub"]["user_id"])
    if user_meta is not None:
        user_meta.delete()
    WPTokenBlocList(jti=jti).save()


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
    sign_in(user.ID, user.user_display_name)
    return jsonify(
        {
            "message": "Авторизация прошла успешно",
            "tokens": user.get_tokens(),
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
    sign_in(user.ID, user_name=user.user_display_name)
    return jsonify(
        {
            "message": "Регистрация прошла успешно",
            "tokens": user.get_tokens(),
            "role": WPRole.get_id(user.role_id).role_name
        }
    ), 200


@blueprint.get('/check_connection')
def check_connection():
    return jsonify(
        {
            "data": "OK"
        }
    )


@blueprint.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    JwtValidator.validate(get_jwt(), {WPRole.ADMIN_NAME, WPRole.USER_NAME, WPRole.EMPLOYEE_NAME})
    
    jwt_identity = get_jwt_identity()
    new_access = create_access_token(identity=jwt_identity)
    
    return jsonify(
        {
            "message": "Авторизация прошла успешно",
            "tokens": {
                "access": new_access,
            },
            "role": WPRole.get_id(get_jwt()["sub"]["role_id"]).role_name
        }
    )

@blueprint.get('/logout')
@jwt_required(verify_type=False)
def logout():
    JwtValidator.validate(get_jwt(), {WPRole.ADMIN_NAME, WPRole.USER_NAME, WPRole.EMPLOYEE_NAME})
    jwt = get_jwt()

    log_out(jwt)
    token_type = jwt['type']

    return jsonify(
        {
            "data": f"{token_type} token revoked successfully"
        }
    ), 200

@blueprint.get('/check_token')
@jwt_required(verify_type=False)
def check_token():
    JwtValidator.validate(get_jwt(), {WPRole.ADMIN_NAME, WPRole.USER_NAME, WPRole.EMPLOYEE_NAME})
    return jsonify(
        {
            "data": "OK",
            "role": WPRole.get_id(get_jwt()["sub"]["role_id"]).role_name
        }
    )
