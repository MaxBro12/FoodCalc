import os
import base64
import hashlib

from .exception import HashLengthException, SecurityException


class SecurityService:
    @staticmethod
    def __create_salt(length: int):
        return os.urandom(length)

    @staticmethod
    def __encode(s: str, encode: str = 'utf-8') -> bytes:
        return base64.b64decode(s)

    @staticmethod
    def __decode(s: bytes, encode: str = 'utf-8') -> str:
        return base64.b64encode(s).decode(encode)

    @classmethod
    def verify(cls, password: str, hashed_password: str, encode: str = 'utf-8') -> bool:
        try:
            algorithm, iterations, stored_hash, salt = hashed_password.split('$')
        except ValueError:
            raise HashLengthException()

        stored_hash = cls.__encode(stored_hash)
        salt = cls.__encode(salt)

        password_hashed = hashlib.pbkdf2_hmac(
            hash_name=algorithm,
            password=password.encode(encode),
            salt=salt,
            iterations=int(iterations),
            dklen=32
        )
        return stored_hash == password_hashed

    @classmethod
    def hash(cls,
        password: str,
        salt: bytes | None = None,
        algorithm: str = 'sha256',
        iterations: int = 100000,
        encode: str = 'utf-8',
        salt_length: int = 16
    ) -> str:
        if salt is None:
            salt = cls.__create_salt(salt_length)
        hashed_password = hashlib.pbkdf2_hmac(
            hash_name=algorithm,
            password=password.encode(encode),
            salt=salt,
            iterations=iterations,
            dklen=32
        )

        return f"{algorithm}${iterations}${cls.__decode(
            hashed_password, encode
        )}${cls.__decode(salt, encode)}"
