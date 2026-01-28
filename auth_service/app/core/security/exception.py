class SecurityException(Exception):
    pass


class HashLengthException(SecurityException):
    def __init__(self):
        super().__init__('Hash length incorrect')
