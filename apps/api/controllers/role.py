from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPRole import WPRole, ADMIN_NAME
from core.domain.schema.RoleSchema import RoleSchema
from ..validators.common import JwtValidator

blueprint = Blueprint('role', __name__, url_prefix="/role")

@blueprint.get('/')
@jwt_required()
def get_roles():
    JwtValidator.validate(get_jwt(), ADMIN_NAME)
    result = RoleSchema().dump(WPRole.get().all(), many=True)
    return jsonify(
        {
            "roles": result
        }
    ), 200
