from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPReserveHistory import WPReserveHistory
from core.domain.schema.SReserveHistory import SReserveHistory
from core.domain.entity import WPRole
from api.validators.common import JwtValidator, PageValidator

blueprint = Blueprint('reserve_history', __name__, url_prefix="/reserve_history")

@blueprint.get('/get')
@jwt_required()
def get_reserve_history():
    JwtValidator.validate(get_jwt(), {WPRole.ADMIN_NAME})
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = SReserveHistory().dump(
        WPReserveHistory.get(
            page_index,
            page_size
        ),
        many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200
