"""
    The small tool to check free space on disks and produce an error if free space is less than specified.
    Disks to check defined by disk letters, so in theory this code is Windows specific.
"""

import os
import re

import psutil
import argparse

from psutil._common import sdiskusage
from sys import exit

MIN_FREE_SPACE_ARGUMENT_NAME = '--min-free-space'
DISKS_ARGUMENT_NAME = '--disks'


def check_disks_free_space():
    disks_input, min_free_space_input = parse_input_arguments()

    if validate_disks_input(disks_input) is False:
        exit(1)

    if validate_min_free_space_input(min_free_space_input) is False:
        announce_error(f'Invalid "{MIN_FREE_SPACE_ARGUMENT_NAME}" input. '
                       f'You must input only a number that represents space in GB (for example, for 10 GB input 10)')
        exit(1)

    min_free_space_GB = int(min_free_space_input)

    if check_min_free_space_input_bounds(disks_input, min_free_space_GB) is False:
        exit(1)

    for disk in disks_input:
        disk_free_space = get_disk_free_space_in_GB(disk)

        if disk_free_space < min_free_space_GB:
            announce_error(f'Not enough free space on disk {disk}: {disk_free_space} GB,'
                           f' minimum required: {min_free_space_input} GB')
            exit(1)

    exit(0)


def parse_input_arguments() -> tuple[list[str], str]:
    args = parse_arguments()
    return args.disks, args.min_free_space[0]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Checks free space on disks')
    parser.add_argument(DISKS_ARGUMENT_NAME, nargs='+', required=True, help='Letters of disks will need be to checked')
    parser.add_argument(MIN_FREE_SPACE_ARGUMENT_NAME, nargs=1, required=True, help='Minimum free space in GB')

    return parser.parse_args()


def validate_disks_input(disks_input: list[str]) -> bool:
    """
        Take into account that validation process is case-sensitive, values of disks must be in upper case
        :param disks_input:
        :return:
    """
    for disk_input in disks_input:
        if re.match(r'^[A-Z]$', disk_input) is False:
            announce_error(f'Invalid "{DISKS_ARGUMENT_NAME}" input.'
                           f' You must input only upper case letters of disks (for example C D E)')
            return False

        if disk_exists(disk_input) is False:
            announce_error(f'Disk {disk_input} does not exist.')
            return False

    return True


def disk_exists(disk_letter: str) -> bool:
    """
        Windows specific code, since it uses first part of a drive path and expects that it's a letter
        :param disk_letter: value is not validated, so make sure that it's valid
        :return:
    """
    for partition in psutil.disk_partitions():
        found_disk_letter, _ = os.path.splitdrive(partition.device)

        # first part of a drive path in Windows is a letter + ':',
        # and since --disks values are just letters, we need to add ':' to the disk_letter
        if found_disk_letter == disk_letter + ':':
            return True

    return False


def validate_min_free_space_input(min_free_space: str) -> bool:
    """
        Take into account - the min_free_space 0 value will be treated as invalid since this is illogical
        :param min_free_space:
        :return:
    """
    return min_free_space.isdigit() and int(min_free_space) > 0


def check_min_free_space_input_bounds(disk_letters: list[str], min_free_space_GB: int) -> bool:
    """
        Windows specific code
        :param disk_letters:
        :param min_free_space_GB: value should be >= 0 to produce correct result
        :return:
    """
    for disk_letter in disk_letters:
        if get_disk_total_space_in_GB(disk_letter) <= min_free_space_GB:
            announce_error(f'Wanted minimum free space is {min_free_space_GB} GB,'
                           f' but disk {disk_letter} has only {get_disk_total_space_in_GB(disk_letter)} GB of total space.')
            return False

    return True


def get_disk_total_space_in_GB(disk_letter: str) -> float:
    """
        Windows specific code
        :param disk_letter:
        :return: not rounded value
    """
    return convert_bytes_to_GB(get_disk_info_by_disk_letter(disk_letter).total)


def get_disk_free_space_in_GB(disk_letter: str) -> float:
    """
        Windows specific code
        :param disk_letter:
        :return: not rounded value
    """
    return convert_bytes_to_GB(get_disk_info_by_disk_letter(disk_letter).free)


def get_disk_info_by_disk_letter(disk_letter: str) -> sdiskusage:
    """
        Windows specific code
        :param disk_letter:
        :return:
    """
    return psutil.disk_usage(f'{disk_letter}:\\')


def convert_bytes_to_GB(value_in_bytes: int) -> float:
    """
        :param value_in_bytes: value should be >= 0 to produce correct result
        :return: not rounded value
    """
    return value_in_bytes / 1024 ** 3


def announce_error(error_message: str):
    os.environ['DISK_CHECK_ERROR'] = error_message
    print(error_message)


if __name__ == '__main__':
    check_disks_free_space()
