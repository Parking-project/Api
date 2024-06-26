import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity import WPUser, WPMessage
from core.domain.schema.SMessage import SMessage
from api.validators import DataExistValidator, IsStr, IsInt, PageValidator, NoneValidator
from api.shared.global_exception import DataError

from config.telegram_config import TelegramConfig

blueprint = Blueprint('message', __name__, url_prefix="/message")

@blueprint.get('/get')
@jwt_required()
def get():
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = SMessage().dump(
        WPMessage.get_message_id(page_index, page_size), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_all')
# @jwt_required()
def get_messages():
    result = SMessage().dump(
        WPMessage.get_all(), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_root')
@jwt_required()
def get_messages_by_root():
    data = request.get_json()
    DataExistValidator(
        {
            "root_id": IsStr() 
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    result = SMessage().dump(
        WPMessage.get_root_id(data["root_id"], page_index, page_size), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_user')
@jwt_required()
def get_messages_by_user():
    data = request.get_json()
    DataExistValidator(
        {
            "user_id": IsStr() 
        }
    ).validate_exist(**data)
    page_index, page_size = PageValidator.validate(**data)
    result = SMessage().dump(
        WPMessage.get_message_id(data["user_id"], page_index, page_size), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200

@blueprint.get('/get_message')
@jwt_required()
def get_message_by_message_id():
    data = request.get_json()
    DataExistValidator(
        {
            "message_id": IsStr() 
        }
    ).validate_exist(**data)
    result = SMessage().dump(
        WPMessage.get_message_id(data["message_id"]), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200


@blueprint.post("/post")
@jwt_required()
def post_message():
    data = request.get_json()

    DataExistValidator(
        {
            "text": IsStr() 
        }
    ).validate_exist(**data)

    message: WPMessage = None
    message_prev: WPMessage = None
    chat_id = TelegramConfig.GROUP_ID
    message_tg_id = None

    if data.get(WPMessage.MESSAGE_BOT_ID) is None:
        message: WPMessage = WPMessage(
            text=data["text"],
            user_id=get_jwt()["sub"]["user_id"],
            chat_id=data.get(WPMessage.CHAT_ID),
            message_tg_id=data.get(WPMessage.MESSAGE_ID)
        )
    else:
        message_prev = NoneValidator().validate(
            key=WPMessage.MESSAGE_BOT_ID,
            value=WPMessage.get_message_bot_tg_id(data[WPMessage.MESSAGE_BOT_ID])
        )
        message: WPMessage = WPMessage(
            text=data["text"],
            user_id=get_jwt()["sub"]["user_id"],
            chat_id=data.get(WPMessage.CHAT_ID),
            message_tg_id=data.get(WPMessage.MESSAGE_ID),
            answer_message_id=message_prev.ID
        )
        
        chat_id = message_prev.message_chat_telegram_id
        message_tg_id = message_prev.message_telegram_id  


    if message.message_answer_id is None or (message_prev is not None and message_prev.is_can_reply()):
        text: str = ""
        user: WPUser = WPUser.get_user_id(message.user_id)
        if user is not None and user.is_user():
            text = f"От: `{user.user_display_name}`\nТекст: "
        text += f"{message.message_text}"
        
        async def send_message():
            bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
            bot_message = await bot.send_message(
                chat_id=chat_id,
                reply_to_message_id=message_tg_id,
                text=text,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            return bot_message.message_id
        message.set_bot_data(
            message_tg_id=asyncio.run(
                send_message()
            ),
            chat_id=chat_id
        )
    message.save()
        
    return jsonify(
        {
            "data": message.ID,
        }
    ), 200

