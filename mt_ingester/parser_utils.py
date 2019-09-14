# coding=utf-8

from typing import Union


def convert_yn_boolean(yn_boolean_raw: str) -> Union[bool, None]:
    """Converts a string with values of `Y` or `N` to the corresponding
    boolean.

    Args:
        yn_boolean_raw (str): A string with values of `Y` or `N`.

    Returns:
        bool: The corresponding boolean or `None` if undefined.
    """

    if yn_boolean_raw == "Y":
        return True
    elif yn_boolean_raw == "N":
        return False
    else:
        return None
