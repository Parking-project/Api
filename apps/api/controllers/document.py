from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import URLInputFile
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity.WPDocument import WPDocument
from core.domain.entity.WPMessage import WPMessage
from core.domain.entity.WPMessageMeta import WPMessageMeta, MESSAGE_BOT_TELEGRAM_ID, MESSAGE_TELEGRAM_ID, MESSAGE_CHAT_TELEGRAM_ID
from core.domain.schema.SDocument import SDocument
from ..validators.common import DataExistValidator, JwtValidator, IsInt, IsStr
from core.domain.entity.WPRole import ADMIN_NAME, USER_NAME, EMPLOYEE_NAME

from config.telegram_config import TelegramConfig
import os
from urllib.parse import urlparse

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

@blueprint.post('/post')
@jwt_required()
def post_document():
    JwtValidator.validate(get_jwt(), {ADMIN_NAME, USER_NAME})
    data = request.get_json()
    DataExistValidator(
        {
            "document_file_id": IsStr(),
            "document_file_unique_id": IsStr(),
            "document_file_size": IsInt(),
            "document_file_url": IsStr(),
            "document_file_mime": IsStr(),
            "message_id": IsStr()
        }
    ).validate_exist(**data)
    document = WPDocument(**data)
    document.save()

    message: WPMessage = WPMessage.get_message_id(document.message_id).first()
    chat_id_send = None
    
    if message.user_id is None:
        chat_id_send = WPMessageMeta.get(message.ID, MESSAGE_CHAT_TELEGRAM_ID)
        if chat_id_send is None:
            return jsonify(
                {
                    "message": "Сообщение сохранено"
                }
            ), 200
    else:
        chat_id_send = TelegramConfig.GROUP_ID
    reply_message_id = WPMessageMeta.get(message.ID, MESSAGE_TELEGRAM_ID)
    
    document = URLInputFile(
        url=document.document_file_url,
        filename=os.path.basename(urlparse(document.document_file_url).path)
    )
    bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
    bot.send_document(
        chat_id_send=TelegramConfig.ADMIN_ID,
        reply_to_message_id=reply_message_id,
        parse_mode=ParseMode.MARKDOWN_V2,
        document=document
    )

    return jsonify(
        {
            "message": "Документ сохранен"
        }
    ), 200
