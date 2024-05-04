from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from core.domain.entity.WPPlace import WPPlace
from core.domain.schema.SPlace import SPlace
from ..validators.common import DataExistValidator, IsStr, IsInt, PageValidator

blueprint = Blueprint('place', __name__, url_prefix="/place")

@blueprint.get('/get_prefix')
@jwt_required()
def get_places_by_prefix():
    data = request.get_json()
    DataExistValidator(
        {
            "place_prefix": IsStr() 
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    result = SPlace().dump(
        WPPlace.get_place_prefix(data.get("place_prefix"), page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_code')
@jwt_required()
def get_place_by_code():
    data = request.get_json()
    DataExistValidator(
        {
            "place_code": IsStr() 
        }
    ).validate_exist(**data)
    result = SPlace().dump(
        WPPlace.get_place_prefix(data.get("place_prefix")).all(), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_free')
@jwt_required()
def get_free_places():
    data = request.get_json()
    DataExistValidator(
        {
            "hours": IsInt() 
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    result = SPlace().dump(
        WPPlace.get_place_prefix(data.get("hours"), page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200
