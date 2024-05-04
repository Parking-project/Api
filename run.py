from application import create_app

app, jwt = create_app()
def main():
    app.run(debug=True, port=9098, host="localhost")

if __name__ == '__main__':
    main()
# import asyncio
# from aiogram import Bot
# from aiogram.enums import ParseMode
# from config.telegram_config import TelegramConfig

# from aiogram.filters.callback_data import CallbackData
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# class TestCallback(CallbackData, prefix='test_callback'):
#     chat_id: int | None
#     message_id: int | None
    


# async def main():
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text="Get Data",
#         callback_data=TestCallback(
#             name="Json City",
#             page_index=None
#         ).pack(),
#     )
#     bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
#     await bot.send_message(
#         chat_id=TelegramConfig.ADMIN_ID,
#         text="test",
#         parse_mode=ParseMode.MARKDOWN_V2,
#         reply_markup=builder.as_markup(resize_keyboard=True)
#     )

# if __name__ == "__main__":
#     asyncio.run(main())
# from aiogram import Bot
# from aiogram.enums import ParseMode
# from aiogram.types import Message
# from flask import Blueprint, jsonify, request
# from flask_jwt_extended import jwt_required, get_jwt
# from core.domain.entity.WPUser import WPUser
# from core.domain.entity.WPMessage import WPMessage
# from core.domain.entity.WPMessageMeta import WPMessageMeta, MESSAGE_BOT_ID, MESSAGE_ID, CHAT_ID
# from core.domain.schema.SMessage import SMessage
# from apps.api.validators.common import DataExistValidator, IsStr, IsInt, PageValidator

# from config.telegram_config import TelegramConfig

# import asyncio

# async def main():
#     bot = Bot(token=TelegramConfig.TOKEN_API, parse_mode=ParseMode.HTML)
#     await bot.send_message(
#         chat_id=TelegramConfig.GROUP_ID,
#         text="Send_Message",
#     )


# if __name__ == '__main__':
#     asyncio.run(main())