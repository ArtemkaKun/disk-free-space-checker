import re


def validate_disks_input(disks_input: list[str]) -> bool:
    if not all(re.match(r'^[A-Z]$', disk) for disk in disks_input):
        return False

    return True
