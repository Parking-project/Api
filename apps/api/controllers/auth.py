from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPAuthHistory import WPAuthHistory
from core.domain.schema.AuthHistorySchema import AuthHistorySchema
from core.domain.entity.WPRole import ADMIN_NAME
from ..validators.common import JwtValidator, PageValidator

blueprint = Blueprint('auth', __name__, url_prefix="/auth")

@blueprint.get('/get')
@jwt_required()
def get_auth_history():
    JwtValidator.validate(get_jwt(), {ADMIN_NAME})
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = AuthHistorySchema().dump(WPAuthHistory.get(page_index, page_size).all(), many=True)
    return jsonify(
        {
            "auth": result
        }
    ), 200
