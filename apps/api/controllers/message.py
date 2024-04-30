from aiogram import Bot
from aiogram.enums import ParseMode
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPMessage import WPMessage
from core.domain.entity.WPMessageMeta import WPMessageMeta, MESSAGE_BOT_TELEGRAM_ID, MESSAGE_TELEGRAM_ID, MESSAGE_CHAT_TELEGRAM_ID
from core.domain.schema.MessageSchema import MessageSchema
from ..validators.common import DataExistValidator, IsStr, IsInt, PageValidator

from config.telegram_config import TelegramConfig

blueprint = Blueprint('message', __name__, url_prefix="/message")

@blueprint.get('/get')
@jwt_required()
def get_messages():
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = MessageSchema().dump(
        WPMessage.get_message_id(page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "messages": result
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
    result = MessageSchema().dump(
        WPMessage.get_message_id(data.get("root_id"), page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "messages": result
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
    result = MessageSchema().dump(
        WPMessage.get_message_id(data.get("user_id"), page_index, page_size).all(), many=True
    )
    return jsonify(
        {
            "messages": result
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
    result = MessageSchema().dump(
        WPMessage.get_message_id(data.get("message_id")).all(), many=True
    )
    return jsonify(
        {
            "messages": result
        }
    ), 200

@blueprint.post("/post")
@jwt_required()
def post_message():
    data = request.get_json()
    message: WPMessage = WPMessage(**data)
    message.save()

    if data.get(MESSAGE_CHAT_TELEGRAM_ID) is not None:
        IsInt.check(data.get(MESSAGE_CHAT_TELEGRAM_ID))
        message_meta = WPMessageMeta(
            key=MESSAGE_CHAT_TELEGRAM_ID, 
            value=data.get(MESSAGE_CHAT_TELEGRAM_ID), 
            message_id=message.ID
        )
        message_meta.save()
    if data.get(MESSAGE_TELEGRAM_ID) is not None:
        IsInt.check(data.get(MESSAGE_TELEGRAM_ID))
        message_meta = WPMessageMeta(
            key=MESSAGE_TELEGRAM_ID, 
            value=data.get(MESSAGE_TELEGRAM_ID), 
            message_id=message.ID
        )
        message_meta.save()

    message_text = ""
    chat_id_send = None
    
    if data.get("user_id") is None:
        chat_id_send = WPMessageMeta.get(message.message_answer_id, MESSAGE_CHAT_TELEGRAM_ID)
        if chat_id_send is None:
            return jsonify(
                {
                    "message": "Сообщение сохранено"
                }
            ), 200
        message_text = message.message_text
    else:
        user = WPUser.get_user_id(data.get("user_id")).first()
        message_text = f"""[Данные пользователя:]\n"
                    f"От: `{user.user_display_name}`\n" 
                    f"Текст сообщения:\n"
                    f"{message.message_text}"""
        chat_id_send = TelegramConfig.GROUP_ID
    reply_message_id = WPMessageMeta.get(message.message_answer_id, MESSAGE_TELEGRAM_ID)

    bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
    bot_message = bot.send_message(
        chat_id=chat_id_send,
        reply_to_message_id=reply_message_id,
        text=message_text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True
    )
        
    message_meta = WPMessageMeta(
        key=MESSAGE_BOT_TELEGRAM_ID, 
        value=bot_message.message_id, 
        message_id=message.ID
    )
    message_meta.save()

    return jsonify(
        {
            "message": "Сообщение сохранено"
        }
    ), 200

