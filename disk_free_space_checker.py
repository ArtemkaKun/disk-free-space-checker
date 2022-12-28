import os
import re

import psutil
import argparse

from psutil._common import sdiskusage


def check_disks_free_space():
    disks_input, min_free_space_input = parse_input_arguments()

    if validate_disks_input(disks_input) is False:
        exit(1)

    if validate_min_free_space_input(min_free_space_input) is False:
        print('Invalid "--min-free-space" input. You must input only a number that represents space in GB (for example, for 10 GB input 10)')
        exit(1)

    min_free_space_GB = int(min_free_space_input)

    if check_min_free_space_input_bounds(min_free_space_GB, disks_input) is False:
        exit(1)

    for disk in disks_input:
        disk_free_space = get_disk_free_space_in_GB(disk)

        if disk_free_space < min_free_space_GB:
            print(f'Not enough free space on disk {disk}: {disk_free_space} GB, minimum required: {min_free_space_input} GB')
            exit(1)

    exit(0)


def parse_input_arguments() -> tuple[list[str], str]:
    args = parse_arguments()
    return args.disks, args.min_free_space[0]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Checks free space on disks')
    parser.add_argument('--disks', nargs='+', required=True, help='Letters of disks will need be to checked')
    parser.add_argument('--min-free-space', nargs=1, required=True, help='Minimum free space in GB')

    return parser.parse_args()


def validate_disks_input(disks: list[str]) -> bool:
    for disk in disks:
        if re.match(r'^[A-Z]$', disk) is False:
            print('Invalid "--disks" input. You must input only letters of disks (for example C D E)')
            return False

        if disk_exists(disk) is False:
            print(f'Disk {disk} does not exist.')
            return False

    return True


def disk_exists(disk_letter):
    for partition in psutil.disk_partitions():
        found_disk_letter, _ = os.path.splitdrive(partition.device)

        if found_disk_letter == disk_letter + ':':
            return True

    return False


def validate_min_free_space_input(min_free_space: str) -> bool:
    return min_free_space.isdigit() and int(min_free_space) > 0


def check_min_free_space_input_bounds(min_free_space_GB: int, disks: list[str]) -> bool:
    for disk in disks:
        if get_disk_total_space_in_GB(disk) <= min_free_space_GB:
            print(f'Wanted minimum free space is {min_free_space_GB} GB, but disk {disk} has only {get_disk_total_space_in_GB(disk)} GB of total space.')
            return False

    return True


def get_disk_total_space_in_GB(disk_letter: str) -> float:
    return convert_bytes_to_GB(get_disk_info_by_disk_letter(disk_letter).total)


def get_disk_free_space_in_GB(disk_letter: str) -> float:
    return convert_bytes_to_GB(get_disk_info_by_disk_letter(disk_letter).free)


def get_disk_info_by_disk_letter(disk_letter: str) -> sdiskusage:
    return psutil.disk_usage(f'{disk_letter}:\\')


def convert_bytes_to_GB(value_in_bytes: int) -> float:
    return value_in_bytes / 1024 ** 3


if __name__ == '__main__':
    check_disks_free_space()
