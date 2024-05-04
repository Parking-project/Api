from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import URLInputFile
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPDocument import WPDocument
from core.domain.entity.WPMessage import WPMessage
from core.domain.entity.WPMessageMeta import WPMessageMeta, MESSAGE_BOT_ID, MESSAGE_ID, CHAT_ID
from core.domain.schema.SDocument import SDocument
from ...shared.global_exception import DataError
from ..validators.common import DataExistValidator, JwtValidator, IsInt, IsStr
from core.domain.entity.WPRole import ADMIN_NAME, USER_NAME, EMPLOYEE_NAME

from config.telegram_config import TelegramConfig
import os
from urllib.parse import urlparse
import asyncio

blueprint = Blueprint('document', __name__, url_prefix="/document")

@blueprint.get('/get')
@jwt_required()
def get_documents_by_message_id():
    JwtValidator.validate(get_jwt(), {ADMIN_NAME, USER_NAME})
    data = request.get_json()
    DataExistValidator(
        {
            "message_id": IsStr() 
        }
    ).validate_exist(**data)
    result = SDocument().dump(WPDocument.get_message_id(data.get("message_id")).all(), many=True)
    return jsonify(
        {
            "documents": result
        }
    ), 200

async def send_message(document: WPDocument, chat_id: int, message_reply_id: int):
    urlInputFile = URLInputFile(
        url=document.document_file_url,
        filename=os.path.basename(urlparse(document.document_file_url).path)
    )
    bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
    await bot.send_document(
        chat_id=chat_id,
        reply_to_message_id=message_reply_id,
        parse_mode=ParseMode.MARKDOWN_V2,
        document=urlInputFile
    )

@blueprint.post('/post')
@jwt_required()
def post_document():
    data = request.get_json()
    DataExistValidator(
        {
            "document_file_url": IsStr(),
            "document_file_mime": IsStr()
        }
    ).validate_exist(**data)
    message = WPMessage.get_first_user_id(
        user_id=get_jwt()["sub"]["user_id"],
    ).first()
    if message is None:
        raise DataError("Сообщение не найдено")
    document = WPDocument(message_id=message.ID, **data)
    document.save()

    message_ID = message.ID
    chat_id = TelegramConfig.GROUP_ID
    message_reply_id: int = None
    print("\n\n\nID = ", message_ID, "\n\n\n")
    print("\n\n\n1) CHAT_ID = ", chat_id)
    print("1) MESSAGE_ID = ", message_reply_id, "\n\n\n")
    if WPMessageMeta.get(message_id=message_ID).count() == 3:
        print("\n\n\n2) CHAT_ID = ", chat_id)
        print("2) MESSAGE_ID = ", message_reply_id, "\n\n\n")
        meta_reply_query = WPMessageMeta.get_bot_message_id(message_ID)
        if meta_reply_query.count() == 0:
            return jsonify(
                {
                    "data": "Документ сохранен"
                }
            ), 200
        message_reply_id = int(meta_reply_query.first().message_meta_value)
        meta_chat = WPMessageMeta.get_group_id(message_ID)
        if meta_chat.count() == 0:
            return jsonify(
                {
                    "data": "Документ сохранен"
                }
            ), 200
        chat_id = int(meta_chat.first().message_meta_value)
    
    print("\n\n\n3) CHAT_ID = ", chat_id)
    print("3) MESSAGE_ID = ", message_reply_id, "\n\n\n")
    asyncio.run(
        send_message(
                document=document, 
                chat_id=chat_id, 
                message_reply_id=message_reply_id
            )
    )
    
    return jsonify(
        {
            "data": "Документ сохранен"
        }
    ), 200
