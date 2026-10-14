from campusflow.exceptions import InvalidAttributeError

from campusflow.types import Categories
from campusflow.types import Urgency
    
def require_non_empty(value: str, field: str):
    if not value.strip():
        raise InvalidAttributeError(f"{field} field cannot be empty.")
    
def check_affected_users(value: str) -> int:
    try:
        int_val = int(value)
    except ValueError:
        raise InvalidAttributeError("Number of affected users must be of type int")

    if int_val <= 0:
        raise InvalidAttributeError("Number of affected users must be greater than zero.")
    
    return int_val
    
def get_category(choice: str):
    
    if choice == "1":
        return Categories.NETWORK.value
    elif choice == "2":
        return Categories.HARDWARE.value
    elif choice == "3":
        return Categories.SOFTWARE.value
    elif choice == "4":
        return Categories.OTHER.value
    else:
        raise InvalidAttributeError("Invalid category selection.")
    
def get_urgency(choice: str):
    
    if choice == "1":
        return Urgency.HIGH.value
    elif choice == "2":
        return Urgency.MEDIUM.value
    elif choice == "3":
        return Urgency.LOW.value
    else:
        raise InvalidAttributeError("Invalid urgency selection.")