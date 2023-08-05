# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilites for datatime module."""
import dateutil
import re

# Regular expressions for date time detection
date_regex1 = re.compile(r'(\d+/\d+/\d+)')
date_regex2 = re.compile(r'(\d+-\d+-\d+)')


def is_known_date_time_format(datetime_str: str) -> bool:
    """
    Check if a given string matches the known date time regular expressions.

    :param datetime_str: Input string to check if it's a date or not
    :return: Whether the given string is in a known date time format or not
    """
    if date_regex1.search(datetime_str) is None and date_regex2.search(datetime_str) is None:
        return False

    return True


def is_date(datetime_str: str) -> bool:
    """
    Check if a given string is a date via parsing through date time parser.

    Needs regex to make sure the dateutil doesn't allow integers
    interpreted as epochs.
    :param datetime_str: Input string to check if it's a date or not
    :return: Whether the given string is a date or not
    """
    try:
        dateutil.parser.parse(datetime_str)
        return True
    except ValueError:
        return False
