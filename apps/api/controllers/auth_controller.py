from flask import Blueprint, jsonify, request
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPTokenBlocList import WPTokenBlocList
from ...shared.request_models import RequestUser
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

blueprint = Blueprint('token', __name__, url_prefix="/token")

@blueprint.post('/login')
def login():
    data = request.get_json()
    user: WPUser = WPUser.authenticate(
        data.get("login"), 
        data.get("password")
    )
    return jsonify(
        {
            "message": "Авторизация прошла успешно",
            "tokens": user.get_tokens()
        }
    )

@blueprint.post('/register')
def register():
    data = request.get_json()
    login: str = data.get("login")
    if WPUser.get_login(login).count() != 0:
        raise Exception("Пользователь с таким логином уже существует!")
    
    user = WPUser(
        login=login,
        password=data.get("password"),
        name=data.get("display_name")
    )
    
    try:
        user.save()
        return jsonify(
            {
                "message": "Регистрация прошла успешно",
                "tokens": user.get_tokens()
            }
        ), 200
    except:
        raise Exception("Регистрация провалилась!")

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