import re

import psutil


def validate_disks_input(disks_input: list[str]) -> bool:
    if not all(re.match(r'^[A-Z]$', disk) for disk in disks_input):
        return False

    return True


def validate_min_space_input(min_free_space: str) -> bool:
    if min_free_space.isdigit() is False or int(min_free_space) < 0:
        return False

    return True


def check_min_free_space_input_bounds(min_free_space: int, disks: list[str]) -> bool:
    for disk in disks:
        if get_disk_total_space_in_GB(disk) <= min_free_space:
            return False

    return True


def get_disk_total_space_in_GB(disk: str) -> float:
    return convert_bytes_to_GB(psutil.disk_usage(f'{disk}:\\').total)


def convert_bytes_to_GB(value_in_bytes: int) -> float:
    return value_in_bytes / 1024**3
