from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from core.domain.entity.WPMessage import WPMessage
from core.domain.schema.MessageSchema import MessageSchema
from ..validators.common import DataExistValidator, IsStr, PageValidator

blueprint = Blueprint('message', __name__, url_prefix="/message")

@blueprint.get('/get')
@jwt_required()
def get():
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = MessageSchema().dump(
        WPMessage.get_message_id(page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "messages": result
        }
    ), 200

@blueprint.get('/get_root')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "root_id": IsStr() 
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    result = MessageSchema().dump(
        WPMessage.get_message_id(data.get("root_id"), page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "messages": result
        }
    ), 200

@blueprint.get('/get_user')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "user_id": IsStr() 
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    result = MessageSchema().dump(
        WPMessage.get_message_id(data.get("user_id"), page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "messages": result
        }
    ), 200

@blueprint.get('/get_message')
@jwt_required()
def get():
    data = request.get_json()
    DataExistValidator(
        {
            "message_id": IsStr() 
        }
    ).validate_exist(**data)
    result = MessageSchema().dump(
        WPMessage.get_message_id(data.get("message_id")).all(), many=True
    )
    return jsonify(
        {
            "messages": result
        }
    ), 200
