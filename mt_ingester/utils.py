# coding=utf-8

import enum


class EnumBase(enum.Enum):
    """Enumeration base-class."""

    @classmethod
    def get_member(
        cls,
        value: str,
    ):
        """Returns an enumeration member with a value matching `value`.

        Args:
            value (str): The value of the member to match.

        Returns:
            The matching member or `None` if `value` is undefined or no member
                was found.
        """

        if not value:
            return None

        members = [
            (member, member.value)
            for member in cls.__members__.values()
        ]
        for member, member_value in members:
            if member_value == value:
                return member

        return None
def return_first_item(func):
    """Decorator that can be used to return the first item of a callable's
    `list` return."""

    # Define the wrapper function.
    def wrapper(self, *args, **kwargs):

        # Execute the decorated method with the provided arguments.
        result = func(self, *args, **kwargs)

        # If the function returned a result and that result is a list then
        # return the first item on that list.
        if result and isinstance(result, list):
            result = result[0]

        return result

    return wrapper
