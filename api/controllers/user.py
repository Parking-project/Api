from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from api.validators.common import JwtValidator, NoneValidator, PageValidator, DataExistValidator, IsInt, IsStr, IsBool, IsExist
from api.shared.global_exception import *
from core.domain.schema import SUser
from core.domain.entity import WPReserve, WPRole, WPPlace, WPUser
from core.domain.enum import ReserveStatus
from config.telegram_config import TelegramConfig

from datetime import datetime, timedelta
from enum import IntEnum, auto
import asyncio

from .base_func import create_dict

blueprint = Blueprint('user', __name__, url_prefix="/user")


@blueprint.get('/get')
@jwt_required()
def get():
    JwtValidator.validate(get_jwt(), [WPRole.USER_NAME])
    user: WPUser = WPUser.get(get_jwt()["sub"]["user_id"])
    result = SUser().dump(
        user,
        many=False
    )
    
    return jsonify(
        {
            "data": result
        }
    ), 200
    
@blueprint.get('/get_all')
# @jwt_required()
def get_all():
    # JwtValidator.validate(get_jwt(), [WPRole.ADMIN_NAME])
    user: WPUser = WPUser.get_all()
    result = SUser().dump(
        user,
        many=False
    )
    
    return jsonify(
        {
            "data": result
        }
    ), 200