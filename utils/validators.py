from typing import Type
from enum import Enum

from campusflow.exceptions import InvalidAttributeError

def validate_value(value: str, valid_values: Type[Enum], field: str):
    # _value2member_map_ is a built-in dict lookup of {value: member}
    if value not in valid_values._value2member_map_:
        raise InvalidAttributeError(f"Invalid {field} value: '{value}'.")
    
def require_non_empty(value: str, field: str):
    if not value.strip():
        raise InvalidAttributeError(f"{field} field cannot be empty.")
    
def check_affected_users(value: str):
    try:
        int(value)
    except ValueError:
        raise InvalidAttributeError("Number of affected users must be of type int")

    if int(value) <= 0:
        raise InvalidAttributeError("Number of affected users must be greater than zero.")