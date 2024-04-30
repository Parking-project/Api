from flask import Blueprint, jsonify, request
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPUserMeta import WPUserMeta
from core.domain.entity.WPTokenBlocList import WPTokenBlocList
from core.domain.entity.WPAuthHistory import WPAuthHistory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from ...shared.global_exception import *
from ..validators.common import NoneValidator, DataExistValidator, IsInt, IsStr
from ..validators.user import UserValidator

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
    user: WPUser = NoneValidator.validate(WPUser.authenticate(**data))
    tokens = user.get_tokens()
    sign_in(user.ID)
    return jsonify(
        {
            "message": "Авторизация прошла успешно",
            "tokens": tokens
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
    new_access_token = create_access_token(identity=identity, expires_delta=24)
    return jsonify(
        {
            "access", new_access_token
        }
    )

@blueprint.get('/logout')
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']
    WPUserMeta.get_user_id(user_id=jwt["sub"]["user_id"]).delete()
    token_b = WPTokenBlocList(jti=jti)

    token_b.save()

    return jsonify(
        {
            "message": f"{token_type} token revoked successfully"
        }
    ), 200