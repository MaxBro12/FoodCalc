from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hashed(plain: str, saved: str):
    return pwd_context.verify(plain, saved)


def unhash(hash_to_str: str):
    return pwd_context.encrypt(hash_to_str)


def get_hash(str_to_hash: str):
    return pwd_context.hash(str_to_hash)
