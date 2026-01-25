from app.core.security import get_hash, verify_hashed


def test_verify_hashed():
    b_str = 'qwerty123456'
    h_str = get_hash(b_str)

    assert verify_hashed(b_str, h_str)


def test_get_hash_returns_bytes():
    result = get_hash("password123")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_hash_different_for_same_input():
    hash1 = get_hash("password123")
    hash2 = get_hash("password123")
    assert hash1 != hash2


def test_verify_hashed_correct_password():
    password = "secure_password"
    hashed = get_hash(password)
    result = verify_hashed(password, hashed)
    assert result is True


def test_verify_hashed_incorrect_password():
    password = "secure_password"
    wrong_password = "wrong_password"
    hashed = get_hash(password)
    result = verify_hashed(wrong_password, hashed)
    assert result is False


def test_verify_hashed_empty_string():
    hashed = get_hash("")
    result = verify_hashed("", hashed)
    assert result is True
    result = verify_hashed("not_empty", hashed)
    assert result is False


def test_verify_hashed_special_characters():
    password = "p@ssw0rd!#$%^&*()"
    hashed = get_hash(password)
    result = verify_hashed(password, hashed)
    assert result is True
    result = verify_hashed("different", hashed)
    assert result is False
