from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from api.validators.common import JwtValidator, NoneValidator, PageValidator, DataExistValidator, IsInt, IsStr, IsBool, IsExist
from api.shared.global_exception import *
from core.domain.schema import SReserve
from core.domain.entity import WPReserve, WPRole, WPPlace, WPUser
from core.domain.enum import ReserveStatus
from config.telegram_config import TelegramConfig

from datetime import datetime, timedelta
from enum import IntEnum, auto
import asyncio

from .base_func import create_dict

blueprint = Blueprint('reserve', __name__, url_prefix="/reserve")


async def send_approve_request(reserve: WPReserve, chat_id: int|None = None, message_id: int|None = None):
    bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)

    class ReserveAction(IntEnum):
        delete = auto()
        approve = auto()
    class BotReserveCallback(CallbackData, prefix='brr'):
        action: ReserveAction
        reserve_id: str
        chat_id: int | None
        message_id: int | None
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="Отклонить",
        callback_data=BotReserveCallback(
            action=ReserveAction.delete,
            reserve_id=str(reserve.ID),
            chat_id=chat_id,
            message_id=message_id
        ).pack(),
    )
    builder.button(
        text="Одобрить",
        callback_data=BotReserveCallback(
            action=ReserveAction.approve,
            reserve_id=str(reserve.ID),
            chat_id=chat_id,
            message_id=message_id
        ).pack(),
    )
    builder.adjust(2)

    user: WPUser = WPUser.get_user_id(reserve.user_id)

    text = f"Пользователь {user.user_display_name} отправил заявку на бронирование \n" +\
        "От " + datetime.fromtimestamp(reserve.reserve_begin).strftime("%d\.%m\.%Y %H:%M:%S") +\
        "    по " + datetime.fromtimestamp(reserve.reserve_begin).strftime("%d\.%m\.%Y %H:%M:%S")
    approve_message = await bot.send_message(
        chat_id=TelegramConfig.RESERVETION_GROUP_ID,
        text=text.encode(),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    return approve_message.message_id

async def delete_approve_message(message_id: int):
    try:
        bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
        await bot.delete_message(
            chat_id=TelegramConfig.RESERVETION_GROUP_ID,
            message_id=message_id
        )
    except:
        return

@blueprint.get('/get')
@jwt_required()
def get_reserve():
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    
    reserves = WPReserve.get(
        page_index=page_index,
        page_size=page_size
    )
    result = SReserve().dump(
        [create_dict(obr, obp) for obr, obp in reserves],
        many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200


# region user get
@blueprint.post('/get_state')
@jwt_required()
def get_state_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.USER_NAME])
    DataExistValidator(
        {
            "reserve_states": IsExist(),
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    
    reserves = WPReserve.get_actual_state(
        user_id=get_jwt()["sub"]["user_id"],
        states=list(data["reserve_states"]),
        page_index=page_index,
        page_size=page_size
    )
    result = SReserve().dump(
        [create_dict(obr, obp) for obr, obp in reserves],
        many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_history_state')
@jwt_required()
def get_history_state_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.USER_NAME])
    DataExistValidator(
        {
            "reserve_states": IsExist(),
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    
    reserves = WPReserve.get_state(
        user_id=get_jwt()["sub"]["user_id"],
        states=list(data["reserve_states"]),
        page_index=page_index,
        page_size=page_size
    )
    result = SReserve().dump(
        [create_dict(obr, obp) for obr, obp in reserves],
        many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get("/get_index")
@jwt_required()
def get_index_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.EMPLOYEE_NAME, WPRole.USER_NAME])
    DataExistValidator(
        {
            "reserve_states": IsExist(),
            "reserve_index": IsInt(),
        }
    ).validate_exist(**data)
    reserve: WPReserve = WPReserve.get_index(
        user_id=get_jwt()["sub"]["user_id"],
        states=list(data["reserve_states"]),
        index=data["reserve_index"]
    )
    obj = SReserve()
    result = obj.dump(reserve, many=False)

    return jsonify(
        {
            "data": result
        }
    ), 200

# endregion

# region post
@blueprint.post('/post_hour')
@jwt_required()
def post_reserve_hour():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.USER_NAME])
    DataExistValidator(
        {
            "hours": IsInt() 
        }
    ).validate_exist(**data)
    curr_datetime = datetime.now()
    reserve: WPReserve = NoneValidator.validate(
        "бронирования",
        WPReserve(
            user_id=get_jwt()["sub"]["user_id"],
            begin=curr_datetime.timestamp(),
            end=(curr_datetime + timedelta(hours=data["hours"])).timestamp()
        )
    )

    message_id = NoneValidator.validate(
        "сообщения телеграм бота",
        asyncio.run(
            send_approve_request(
                reserve=reserve,
                chat_id=data.get("chat_id"),
                message_id=data.get("message_id")
            )
        )
    )
    reserve.set_message_id(message_id)
    
    reserve.save()
    return jsonify(
        {
            "data": {
                "message_id": message_id,
                "reserve_id": reserve.ID
            }
        }
    ), 200

@blueprint.post('/post_dates')
@jwt_required()
def post_reserve_dates():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), WPRole.USER_NAME)
    DataExistValidator(
        {
            "begin": IsInt(),
            "end": IsInt()
        }
    ).validate_exist(**data)
    reserve = WPReserve(
        user_id=get_jwt()["sub"]["user_id"],
        begin=data["begin"],
        end=data["end"]
    )
    reserve.save()

    return jsonify(
        {
            "data": asyncio.run(
                send_approve_request(reserve=reserve)
            )
        }
    ), 200


@blueprint.post('/approve')
@jwt_required()
def approve_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.EMPLOYEE_NAME])
    DataExistValidator(
        {
            "reserve_id": IsStr(),
        }
    ).validate_exist(**data)
    reserve: WPReserve = NoneValidator.validate(
        "бронирования",
        WPReserve.get_reserve_id(data["reserve_id"])
    )
    if reserve.reserve_message_id is not None:
        message_id = reserve.reserve_message_id
        reserve.set_message_id(None)
        asyncio.run(delete_approve_message(message_id))
    reserve.approving()
    return jsonify(
        {
            "data": "Заявка успешно одобрена"
        }
    ), 200

@blueprint.post('/delete')
@jwt_required()
def delete_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.EMPLOYEE_NAME, WPRole.USER_NAME])
    DataExistValidator(
        {
            "reserve_id": IsStr(),
        }
    ).validate_exist(**data)
    reserve: WPReserve = NoneValidator.validate(
        "бронирования",
        WPReserve.get_reserve_id(data["reserve_id"])
    )
    if reserve.reserve_message_id is not None:
        message_id = reserve.reserve_message_id
        reserve.set_message_id(None)
        asyncio.run(delete_approve_message(message_id))
    reserve.delete()
    reserve.save()
    return jsonify(
        {
            "data": "Заявка успешно отклонена"
        }
    ), 200

@blueprint.post('/delete_index')
@jwt_required()
def delete_index_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.EMPLOYEE_NAME, WPRole.USER_NAME])
    DataExistValidator(
        {
            "reserve_index": IsInt(),
        }
    ).validate_exist(**data)
    if data["reserve_index"] < 0:
        raise DataError("Номер не может быть меньше 0")
    reserve: WPReserve = NoneValidator.validate(
        "бронирования",
        WPReserve.get_index(
            user_id=get_jwt()["sub"]["user_id"],
            states=[2,3],
            index=data["reserve_index"]
        )
    )
    if reserve.reserve_message_id is not None:
        message_id = reserve.reserve_message_id
        reserve.set_message_id(None)
        asyncio.run(delete_approve_message(message_id))
    reserve.delete()
    return jsonify(
        {
            "data": "Заявка успешно удалена"
        }
    ), 200

@blueprint.post('/set_place')
@jwt_required()
def set_place_reserve():
    data = request.get_json()
    JwtValidator.validate(get_jwt(), [WPRole.EMPLOYEE_NAME, WPRole.USER_NAME])
    DataExistValidator(
        {
            "reserve_id": IsStr(),
            "place_code": IsStr(),
        }
    ).validate_exist(**data)
    reserve: WPReserve = NoneValidator.validate(
        "бронирования",
        WPReserve.get_reserve_id(data["reserve_id"])
    )
    place: WPPlace = NoneValidator.validate(
        "парковочного места",
        WPPlace.get_place_code(data["place_code"])
    )
    try:
        reserve.set_place(place.ID)
        reserve.save()
    except:
        raise DataError("Невозможно выбрать данное парковочное места так как на период бронирования оно занято!")
    return jsonify(
        {
            "data": f"""Для заявки {datetime.fromtimestamp(reserve.reserve_begin).strftime("%d.%m.%Y %H:%M:%S")} - {datetime.fromtimestamp(reserve.reserve_begin).strftime("%d.%m.%Y %H:%M:%S")}
        Было установленно парковочное место: {place.place_code}"""
        }
    ), 200

# endregion