from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt


blueprint = Blueprint('token', __name__, url_prefix="/token")