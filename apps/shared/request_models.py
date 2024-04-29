from datetime import datetime

class RequestMessage:
    date: float
    user_id: int | None
    user_telegram_id: int
    message_telegram_id: int
    bot_message_telegram_id: int

    text: str | None
    answer_id: int | None

    def __init__(self, date: datetime, user_id: int | None, user_telegram_id: int,
                 message_telegram_id: int, bot_message_telegram_id: int,
                 text: str | None, answer_id: int | None):
        self.date = date.utcnow().timestamp(),
        self.text = text
        self.user_id = user_id
        self.answer_id = answer_id
        self.user_telegram_id = user_telegram_id
        self.message_telegram_id = message_telegram_id
        self.bot_message_telegram_id = bot_message_telegram_id

class RequestDocument:
    message_id: int
    id: int
    unique_id: int
    size: int
    url: str
    mime: str

    def __init__(self, message_id: int, file_id: int,
                 file_unique_id: int, file_size: int,
                 file_url: str, file_mime: str):
        self.message_id = message_id
        self.id = file_id
        self.unique_id = file_unique_id
        self.size = file_size
        self.url = file_url
        self.mime = file_mime

class RequestUser:
    login: str
    password: str
    display_name: str
    telephone: str