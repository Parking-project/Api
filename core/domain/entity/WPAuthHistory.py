from extensions.databse_extension import Base
from ..interface import IWPAuthHistory

class WPAuthHistory(Base, IWPAuthHistory):
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    @classmethod
    def get(cls):
        pass
