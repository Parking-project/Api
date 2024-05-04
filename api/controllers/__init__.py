__all__ = (
    "auth_bp",
    "document_bp",
    "message_bp",
    "place_bp",
    "reserve_history_bp",
    "reserve_bp",
    "role_bp",
    "token_bloc_list_bp",
    "token_bp",
    "user_bp"
)

from .auth import blueprint as auth_bp
from .document import blueprint as document_bp
from .message import blueprint as message_bp
from .place import blueprint as place_bp
from .reserve_history import blueprint as reserve_history_bp
from .reserve import blueprint as reserve_bp
from .role import blueprint as role_bp
from .token_bloc_list import blueprint as token_bloc_list_bp
from .token import blueprint as token_bp
from .user import blueprint as user_bp
