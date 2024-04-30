from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPReserveHistory import WPReserveHistory
from core.domain.schema.ReserveHistorySchema import ReserveHistorySchema
from core.domain.entity.WPRole import ADMIN_NAME
from ..validators.common import JwtValidator, PageValidator

blueprint = Blueprint('reserve_history', __name__, url_prefix="/reserve_history")

@blueprint.get('/get')
@jwt_required()
def get():
    JwtValidator.validate(get_jwt(), {ADMIN_NAME})
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = ReserveHistorySchema().dump(WPReserveHistory.get(page_index, page_size).all(), many=True)
    return jsonify(
        {
            "reserve_history": result
        }
    ), 200
