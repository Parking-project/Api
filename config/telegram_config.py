"""Flask config class."""
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramConfig:
    TOKEN_API: str = os.getenv('TOKEN_API')
    ADMIN_ID: int = os.getenv('ADMIN_ID')
    GROUP_ID: str = os.getenv('GROUP_ID')
    RESERVETION_GROUP_ID: str = os.getenv('RESERVETION_GROUP_ID')
