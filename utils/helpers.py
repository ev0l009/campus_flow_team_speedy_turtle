import secrets
import string

from campusflow.ui import category_menu
from campusflow.ui import urgency_menu

from campusflow.types import Categories
from campusflow.types import Urgency

from campusflow.exceptions import InvalidAttributeError

def generate_prefixed_id(preffix: str, length: int = 5):
    character_pool = string.ascii_letters + string.digits
    suffix = ''.join(secrets.choice(character_pool) for _ in range(length))
    return f"{preffix}_{suffix}"

def get_category():
    choice = input(category_menu)
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
    
def get_urgency():
    choice = input(urgency_menu)
    if choice == "1":
        return Urgency.HIGH.value
    elif choice == "2":
        return Urgency.MEDIUM.value
    elif choice == "3":
        return Urgency.LOW.value
    else:
        raise InvalidAttributeError("Invalid urgency selection.")