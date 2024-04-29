from ...shared.global_exception import SecurityError
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPRole import WPRole

class JwtValidator:
    @classmethod
    def validate(cls, jwt, role_name):
        user = WPUser.get_user_id(jwt["sub"]["user_id"]).first()
        role = WPRole.get_id(jwt["sub"]["role_id"]).first()
        if user is not None and role is not None:
            if role.role_name == role_name:
                return
        raise SecurityError()