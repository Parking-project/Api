from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPDocument import WPDocument
from core.domain.schema.DocumentSchema import DocumentSchema
from ..validators.common import DataExistValidator, JwtValidator, IsInt, IsStr
from core.domain.entity.WPRole import ADMIN_NAME, USER_NAME, EMPLOYEE_NAME

blueprint = Blueprint('document', __name__, url_prefix="/document")

@blueprint.get('/get')
@jwt_required()
def get():
    JwtValidator.validate(get_jwt(), {ADMIN_NAME, USER_NAME})
    data = request.get_json()
    DataExistValidator(
        {
            "message_id": IsStr() 
        }
    ).validate_exist(**data)
    result = DocumentSchema().dump(WPDocument.get_message_id(data.get("message_id")).all(), many=True)
    return jsonify(
        {
            "documents": result
        }
    ), 200

@blueprint.post('/post')
@jwt_required()
def post():
    data = request.get_json()
    DataExistValidator(
        {
            "document_file_id": IsStr(),
            "document_file_unique_id": IsStr(),
            "document_file_size": IsInt(),
            "document_file_url": IsStr(),
            "document_file_mime": IsStr(),
            "message_id": IsStr()
        }
    ).validate_exist(**data)
    document = WPDocument(**data)
    document.save()
    return jsonify(
        {
            "message": "Документ сохранен"
        }
    ), 200
