from disk_free_space_checker import validate_min_free_space_input


def test_validate_letter_min_space_input_false():
    assert validate_min_free_space_input('A') is False


def test_validate_empty_min_space_input_false():
    assert validate_min_free_space_input('') is False


def test_validate_special_character_min_space_input_false():
    assert validate_min_free_space_input('@') is False


def test_validate_injection_min_space_input_false():
    assert validate_min_free_space_input('100;') is False


def test_validate_malicious_code_min_space_input_false():
    assert validate_min_free_space_input('eval') is False


def test_validate_negative_min_space_input_false():
    assert validate_min_free_space_input('-100') is False


def test_validate_zero_min_space_input_false():
    assert validate_min_free_space_input('0') is False


def test_validate_correct_min_space_input_true():
    assert validate_min_free_space_input('100') is True
