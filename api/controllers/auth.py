from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPAuthHistory import WPAuthHistory
from core.domain.schema.SAuthHistory import SAuthHistory
from core.domain.entity import WPRole
from api.validators.common import JwtValidator, PageValidator

blueprint = Blueprint('auth', __name__, url_prefix="/auth")

@blueprint.get('/get')
@jwt_required()
def get_auth_history():
    JwtValidator.validate(get_jwt(), {WPRole.ADMIN_NAME})
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = SAuthHistory().dump(WPAuthHistory.get(page_index, page_size), many=True)
    return jsonify(
        {
            "data": result
        }
    ), 200
