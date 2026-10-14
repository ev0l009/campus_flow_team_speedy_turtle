from enum import Enum
from typing import TypedDict

class Categories(Enum):
    NETWORK = "Network"
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    OTHER = "Other"

class Urgency(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in progress"
    RESOLVED = "resolved"

class TicketDictType(TypedDict):
    id: str
    title: str
    category: str
    urgency: str
    affected_users: int
    priority: str
    status: str
    assigned_to: str | None