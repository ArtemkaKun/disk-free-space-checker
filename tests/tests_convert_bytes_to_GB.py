import math

from disk_free_space_checker import convert_bytes_to_GB


def test_convert_bytes_to_GB():
    assert math.isclose(convert_bytes_to_GB(1073741824), 1.0, rel_tol=1e-6) is True
