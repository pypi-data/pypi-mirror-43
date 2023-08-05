
class GenericException(Exception):
    def __init__(self, *args, key, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key


class MeosAppException(GenericException):
    pass
