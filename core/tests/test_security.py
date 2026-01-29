import pytest
from core.security import SecurityService, HashLengthException


def test_verify_hashed():
    b_str = 'qwerty123456'
    h_str = SecurityService.hash(b_str)
    assert SecurityService.verify(b_str, h_str)


def test_get_hash_returns_str():
    result = SecurityService.hash("password123")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_hash_different_for_same_input():
    password = "password123"
    hash1 = SecurityService.hash(password)
    hash2 = SecurityService.hash(password)
    assert hash1 != hash2


def test_verify_hashed_incorrect_password():
    password = "secure_password"
    wrong_password = "wrong_password"
    hashed = SecurityService.hash(password)
    assert SecurityService.verify(wrong_password, hashed) is False


def test_verify_hashed_empty_string():
    hashed = SecurityService.hash("")
    assert SecurityService.verify("", hashed) is True
    assert SecurityService.verify("not_empty", hashed) is False


def test_verify_hashed_special_characters():
    password = "p@ssw0rd!#$%^&*()"
    hashed = SecurityService.hash(password)
    assert SecurityService.verify(password, hashed) is True
    assert SecurityService.verify("different", hashed) is False


def test_verify_hashed_raises_exception_on_invalid_input():
    try:
        SecurityService.verify('test', "")
    except HashLengthException:
        assert True
    else:
        assert False
