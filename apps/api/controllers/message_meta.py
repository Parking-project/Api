from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from core.domain.entity.WPMessageMeta import WPMessageMeta
from core.domain.schema.MessageMetaSchema import MessageMetaSchema
from ..validators.common import DataExistValidator, IsInt, IsStr

blueprint = Blueprint('message_meta', __name__, url_prefix="/message_meta")

@blueprint.get('/get_message')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "message_id": IsStr()
        }
    ).validate_exist(**data)
    result = MessageMetaSchema().dump(
        WPMessageMeta.get_message_id(data.get("message_id")).all(), many=True
    )
    return jsonify(
        {
            "message_meta": result
        }
    ), 200

@blueprint.get('/get_tg_bot')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "tg_bot_id": IsInt()
        }
    ).validate_exist(**data)
    result = MessageMetaSchema().dump(
        WPMessageMeta.get_tg_bot_id(data.get("tg_bot_id")).all(), many=True
    )
    return jsonify(
        {
            "message_meta": result
        }
    ), 200

@blueprint.get('/get_tg')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "tg_id": IsInt()
        }
    ).validate_exist(**data)
    result = MessageMetaSchema().dump(
        WPMessageMeta.get_tg_bot_id(data.get("tg_id")).all(), many=True
    )
    return jsonify(
        {
            "message_meta": result
        }
    ), 200

@blueprint.get('/get_user')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "tg_user_id": IsInt()
        }
    ).validate_exist(**data)
    result = MessageMetaSchema().dump(
        WPMessageMeta.get_tg_bot_id(data.get("tg_user_id")).all(), many=True
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
            "message_meta_key": IsStr(),
            "message_meta_value": IsStr(),
            "message_id": IsStr()
        }
    ).validate_exist(**data)
    message_meta = WPMessageMeta(**data)
    message_meta.save()
    return jsonify(
        {
            "message": "Мета данные сохранены"
        }
    ), 200
