from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from core.domain.entity.WPRole import WPRole

blueprint = Blueprint('role', __name__, url_prefix="/role")