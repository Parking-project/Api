from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from core.domain.entity import WPPlace, WPReserve
from core.domain.schema import SPlace
from api.validators.common import DataExistValidator, IsStr, IsInt, PageValidator, NoneValidator

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
        WPPlace.get_place_prefix(data["place_prefix"], page_index, page_size),
        many=True
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
        WPPlace.get_place_code(data["place_code"]), many=False
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_free_id')
@jwt_required()
def get_free_id_places():
    data = request.get_json()
    DataExistValidator(
        {
            "reserve_id": IsStr(),
        }
    ).validate_exist(**data)

    page_index, page_size = PageValidator.validate(**data)

    reserve: WPReserve = NoneValidator.validate(
        "бронирования",
        WPReserve.get_reserve_id(data["reserve_id"])
    )

    reserves = WPReserve.get_time_period(
        reserve.reserve_begin,
        reserve.reserve_end,
    )
    result = SPlace().dump(
        WPPlace.get_free(
            reserves,
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

@blueprint.get('/get_free_period')
@jwt_required()
def get_free_period_places():
    data = request.get_json()
    DataExistValidator(
        {
            "reserve_begin": IsInt(),
            "reserve_end": IsInt(),
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)

    reserves = WPReserve.get_time_period(
        data["reserve_begin"],
        data["reserve_end"],
    )
    result = SPlace().dump(
        WPPlace.get_free(
            reserves,
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
