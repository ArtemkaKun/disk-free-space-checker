from disk_free_space_checker import validate_disks_input


def test_validate_numerical_disks_input_false():
    assert validate_disks_input(['1']) is False


def test_validate_special_characters_disks_input_false():
    assert validate_disks_input(['@']) is False


def test_validate_empty_disks_input_false():
    assert validate_disks_input(['']) is False


def test_validate_double_letter_disks_input_false():
    assert validate_disks_input(['AA']) is False


def test_validate_injection_disks_input_false():
    assert validate_disks_input(['A;']) is False


def test_validate_malicious_code_disks_input_false():
    assert validate_disks_input(['eval', 'os.']) is False
