import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPMessage import WPMessage
from core.domain.entity.WPMessageMeta import WPMessageMeta, MESSAGE_BOT_ID, MESSAGE_ID, CHAT_ID
from core.domain.schema.SMessage import SMessage
from ..validators.common import DataExistValidator, IsStr, IsInt, PageValidator

from config.telegram_config import TelegramConfig

blueprint = Blueprint('message', __name__, url_prefix="/message")

@blueprint.get('/get')
@jwt_required()
def get_messages():
    data = request.get_json()
    page_index, page_size = PageValidator.validate(**data)
    result = SMessage().dump(
        WPMessage.get_message_id(page_index, page_size).all(), many=True
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
        WPMessage.get_message_id(data.get("root_id"), page_index, page_size).all(), many=True
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
        WPMessage.get_message_id(data.get("user_id"), page_index, page_size).all(), many=True
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
        WPMessage.get_message_id(data.get("message_id")).all(), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200


def save_message_meta(key: str, value: int, message_id: int):
    WPMessageMeta(
        key=key, 
        value=str(value), 
        message_id=message_id
    ).save()

async def send_message(text: str, chat_id: int, message_id: int):
    bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
    bot_message = await bot.send_message(
        chat_id=chat_id,
        reply_to_message_id=message_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return bot_message.message_id

@blueprint.post("/post_group")
@jwt_required()
def post_employee_message():
    data = request.get_json()
    DataExistValidator(
        {
            "text": IsStr(),
            MESSAGE_ID: IsInt(),
            MESSAGE_BOT_ID: IsInt(),
            CHAT_ID: IsInt(),
        }
    ).validate_exist(**data)

    message_meta: WPMessageMeta = WPMessageMeta.get_by_message_tg_id(data[MESSAGE_BOT_ID]).first()
    message: WPMessage = WPMessage(
        data["text"],
        get_jwt()["sub"]["user_id"],
        message_meta.message_id
    )
    message.save()

    save_message_meta(CHAT_ID, data[CHAT_ID])
    save_message_meta(MESSAGE_ID, data[MESSAGE_ID])


    if WPMessageMeta.get(message_id=message_meta.message_id).count() == 3:
        save_message_meta(
            MESSAGE_BOT_ID,
            asyncio.run(
                send_message(
                    text=message.message_text, 
                    chat_id=int(WPMessageMeta.get_group_id(message_meta.message_id).first().message_meta_value),
                    message_id=int(WPMessageMeta.get_message_id(message_meta.message_id).first().message_meta_value),
                )
            )
        )

@blueprint.post("/post_chat")
@jwt_required()
def post_user_message():
    data = request.get_json()
    message: WPMessage = None
    answer_id = None
    DataExistValidator({"text": IsStr()}).validate_exist(**data)

    if data.get(MESSAGE_BOT_ID) is None:
        message: WPMessage = WPMessage(
            text=data["text"],
            user_id=get_jwt()["sub"]["user_id"]
        )
    else:
        message_meta = WPMessageMeta.get_by_message_tg_id(data[MESSAGE_BOT_ID])
        message: WPMessage = WPMessage(
            text=data["text"],
            user_id=get_jwt()["sub"]["user_id"],
            answer_message_id=(message_meta.count() == 0 if None else message_meta.message_id)
        )
        chat_id=int(WPMessageMeta.get_group_id(message_meta.message_id).first().message_meta_value),
        message_meta = WPMessageMeta.get_message_id(message_meta.message_id)
        answer_id = (message_meta.count() == 0 if None else int(message_meta.first().message_meta_value))    
        
    message.save()
    if data.get(CHAT_ID) is not None and data.get(MESSAGE_ID) is not None:
        save_message_meta(CHAT_ID, data[CHAT_ID], message.ID)
        save_message_meta(MESSAGE_ID, data[MESSAGE_ID], message.ID)
    save_message_meta(
        MESSAGE_BOT_ID,
        asyncio.run(
            send_message(
                text=message.message_text, 
                chat_id=TelegramConfig.GROUP_ID,
                message_id=answer_id,
            )
        ), 
        message.ID
    )
    return jsonify(
        {
            "data": "Сообщение сохранено"
        }
    ), 200

