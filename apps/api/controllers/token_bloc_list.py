from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPTokenBlocList import WPTokenBlocList
from core.domain.schema.STokenBlocList import STokenBlocList
from core.domain.entity.WPRole import ADMIN_NAME
from ..validators.common import JwtValidator, PageValidator

blueprint = Blueprint('token_bloc_list', __name__, url_prefix="/token_bloc_list")

@blueprint.get('/get')
@jwt_required()
def get_bloc_tokens():
    JwtValidator.validate(get_jwt(), {ADMIN_NAME})
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = STokenBlocList().dump(WPTokenBlocList.get(page_index, page_size).all(), many=True)
    return jsonify(
        {
            "reserve_history": result
        }
    ), 200

