from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from core.domain.entity import WPDocument,WPMessage
from core.domain.schema import SDocument
from api.shared.global_exception import DataError
from api.validators.common import DataExistValidator, JwtValidator, IsInt, IsStr
from core.domain.entity import WPRole

from config.telegram_config import TelegramConfig
import os
import io
from urllib.parse import urlparse
import asyncio

blueprint = Blueprint('document', __name__, url_prefix="/document")

@blueprint.get('/get')
@jwt_required()
def get_documents_by_message_id():
    JwtValidator.validate(get_jwt(), {WPRole.ADMIN_NAME, WPRole.USER_NAME})
    data = request.get_json()
    DataExistValidator(
        {
            "message_id": IsStr() 
        }
    ).validate_exist(**data)
    result = SDocument().dump(WPDocument.get_message_id(data.get("message_id")), many=True)
    return jsonify(
        {
            "documents": result
        }
    ), 200


@blueprint.post('/post')
@jwt_required()
def post_document():
    data = request.get_json()
    DataExistValidator(
        {
            "document_file_id": IsStr(),
            "document_file_unique_id": IsStr(),
            "document_file_size": IsInt(),
            "document_file_url": IsStr(),
            "document_file_mime": IsStr()
        }
    ).validate_exist(**data)
    message: WPMessage = WPMessage.get_last_user_id(
        user_id=get_jwt()["sub"]["user_id"],
    )
    if message is None:
        raise DataError("Сообщение не найдено")
    document = WPDocument(message_id=message.ID, **data)
    document.save()
    if not message.is_can_reply():
        return jsonify(
            {
                "data": "Документ сохранен"
            }
        ), 200
    
    async def send_document():
        bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
        file = await bot.get_file(document.document_file_id)
        file_in_io = io.BytesIO()
        await bot.download_file(file.file_path, destination=file_in_io)
        file_bytes = file_in_io.read(document.document_file_size)

        await bot.send_document(
            chat_id=message.message_bot_chat_telegram_id,
            reply_to_message_id=message.message_bot_telegram_id,
            parse_mode=ParseMode.MARKDOWN_V2,
            document=BufferedInputFile(file_bytes, filename=os.path.basename(urlparse(document.document_file_url).path))
        )
    asyncio.run(send_document())
    
    return jsonify(
        {
            "data": "Документ сохранен"
        }
    ), 200
