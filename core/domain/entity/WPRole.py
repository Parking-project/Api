from extensions.databse_extension import Base
from ..interface import IWPRole

class WPRole(IWPRole):
    @classmethod
    def get_id(cls, role_id: str):
        pass

    @classmethod
    def get_name(cls, role_name: str):
        pass
