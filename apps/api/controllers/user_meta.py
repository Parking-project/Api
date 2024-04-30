from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from core.domain.entity.WPUserMeta import WPUserMeta
from core.domain.schema.UserMetaSchema import UserMetaSchema
from ..validators.common import DataExistValidator, IsInt, IsStr

blueprint = Blueprint('user_meta', __name__, url_prefix="/user_meta")

@blueprint.get('/get_user')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "user_id": IsStr()
        }
    ).validate_exist(**data)
    result = UserMetaSchema().dump(
        WPUserMeta.get_user_id(data.get("user_id")).all(), many=True
    )
    return jsonify(
        {
            "message_meta": result
        }
    ), 200

@blueprint.get('/get_tg_id')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "telegram_id": IsInt()
        }
    ).validate_exist(**data)
    result = UserMetaSchema().dump(
        WPUserMeta.get_telegram_id(data.get("telegram_id")).all(), many=True
    )
    return jsonify(
        {
            "message_meta": result
        }
    ), 200

@blueprint.post('/post')
@jwt_required()
def post():
    data = request.get_json()
    DataExistValidator(
        {
            "user_id": IsStr(),
            "telegram_id": IsInt()
        }
    ).validate_exist(**data)
    message_meta = WPUserMeta(**data)
    message_meta.save()
    return jsonify(
        {
            "message": "Мета данные сохранены"
        }
    ), 200
