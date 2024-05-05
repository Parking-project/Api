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
def get_messages():
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
        WPMessage.get_message_id(data.get("root_id"), page_index, page_size), many=True
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
        WPMessage.get_message_id(data.get("user_id"), page_index, page_size), many=True
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
        WPMessage.get_message_id(data.get("message_id")), many=True
    )
    return jsonify(
        {
            "data": result
        }
    ), 200


async def send_message(text: str, chat_id: int, message_tg_id: int):
    bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
    bot_message = await bot.send_message(
        chat_id=chat_id,
        reply_to_message_id=message_tg_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return bot_message.message_id

# @blueprint.post("/post_group")
# @jwt_required()
# def post_employee_message():
#     data = request.get_json()
#     DataExistValidator(
#         {
#             "text": IsStr(),
#             WPMessageMeta.MESSAGE_ID: IsInt(),
#             WPMessageMeta.MESSAGE_BOT_ID: IsInt(),
#             WPMessageMeta.CHAT_ID: IsInt(),
#         }
#     ).validate_exist(**data)

#     message_meta: WPMessageMeta = WPMessageMeta.get_by_message_tg_id(data[WPMessageMeta.MESSAGE_BOT_ID])
#     message: WPMessage = WPMessage(
#         data["text"],
#         get_jwt()["sub"]["user_id"],
#         message_meta.message_id
#     )
#     message.save()

#     save_message_meta(WPMessageMeta.CHAT_ID, data[WPMessageMeta.CHAT_ID])
#     save_message_meta(WPMessageMeta.MESSAGE_ID, data[WPMessageMeta.MESSAGE_ID])


#     if WPMessageMeta.get(message_id=message_meta.message_id).count() == 3:
#         save_message_meta(
#             WPMessageMeta.MESSAGE_BOT_ID,
#             asyncio.run(
#                 send_message(
#                     text=message.message_text, 
#                     chat_id=int(WPMessageMeta.get_group_id(message_meta.message_id).first().message_meta_value),
#                     message_id=int(WPMessageMeta.get_message_id(message_meta.message_id).first().message_meta_value),
#                 )
#             )
#         )

@blueprint.post("/post")
@jwt_required()
def post_user_message():
    data = request.get_json()
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
            answer_message_id=(message_prev is None if None else message.ID)
        )
        
        chat_id = message.message_chat_telegram_id
        message_tg_id = message.message_telegram_id  

    if message.message_answer_id is None or \
       (message_prev is not None and message_prev.is_can_reply()):
        text: str = ""
        user: WPUser = WPUser.get_user_id(message.user_id)
        if user is not None and not user.is_user():
            text = f"От: `{user.user_display_name}`\n"
        text += f"Текст: {message.message_text}"
        message.set_bot_data(
            message_tg_id=asyncio.run(
                send_message(
                    text=text, 
                    chat_id=chat_id,
                    message_tg_id=message_tg_id,
                )
            ),
            chat_id=chat_id
        )
    message.save()
        
    return jsonify(
        {
            "data": "Сообщение сохранено",
            "message_id": message.ID
        }
    ), 200

