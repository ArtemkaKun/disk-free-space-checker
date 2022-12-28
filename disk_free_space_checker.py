import re


def validate_disks_input(disks_input: list[str]) -> bool:
    if not all(re.match(r'^[A-Z]$', disk) for disk in disks_input):
        return False

    return True


def validate_min_space_input(min_free_space: str) -> bool:
    if min_free_space.isdigit() is False or int(min_free_space) < 0:
        return False

    return True
