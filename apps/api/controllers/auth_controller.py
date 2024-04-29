from flask import Blueprint, jsonify, request
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPTokenBlocList import WPTokenBlocList
from ...shared.request_models import RequestUser
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from ...shared.global_exception import *
from ..validators.user_validate import UserValidator
from ..validators.none_validate import NoneValidator

blueprint = Blueprint('token', __name__, url_prefix="/token")

@blueprint.post('/login')
def login():
    data = request.get_json()
    user: WPUser = NoneValidator.validate(WPUser.authenticate(**data))
    return jsonify(
        {
            "message": "Авторизация прошла успешно",
            "tokens": user.get_tokens()
        }
    )

@blueprint.post('/register')
def register():
    data = request.get_json()
    UserValidator.validate_register(**data)
    UserValidator.validate_unique(**data)
        
    user = WPUser(**data)
    user.save()
    return jsonify(
        {
            "message": "Регистрация прошла успешно",
            "tokens": user.get_tokens()
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

    token_b = WPTokenBlocList(jti=jti)

    token_b.save()

    return jsonify(
        {
            "message": f"{token_type} token revoked successfully"
        }
    ), 200