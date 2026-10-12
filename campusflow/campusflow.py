from pathlib import Path
import json

import os

from utils.helpers import generate_prefixed_id

from utils.validators import require_non_empty
from utils.validators import validate_value
from utils.validators import check_affected_users

from campusflow.exceptions import InvalidTicketIDError
from campusflow.exceptions import DatabaseError

from collections import Counter

from campusflow.types import CampusFlowDict, TicketDictType, Categories, Urgency, TicketStatus

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_FILE_PATH = DB_DIR / "tickets.json"


class CampusFlow:
    
    PRIORITY_ORDER = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    }

    def __init__(self) -> None:
        self.data: CampusFlowDict = {
            "tickets": {},
            "staff": {}
        }
        self.ticket_ids = list(self.data["tickets"])

    def create_ticket(
        self, 
        title: str, 
        category: str, 
        urgency: str, 
        affected_users: str
    ):
        require_non_empty(title, "Title")
        validate_value(category, Categories, "Category")
        validate_value(urgency, Urgency, "Urgency")
        check_affected_users(affected_users)
 
        ticket_id = generate_prefixed_id("tkt")

        self.data["tickets"][ticket_id]  = {
            "id": ticket_id,
            "title": title,
            "category": category,
            "urgency": urgency,
            "affected_users": int(affected_users),
            "priority": self.calculate_priority(int(affected_users), urgency),
            "status": TicketStatus.OPEN.value,
            "assigned_to": None   
        }

    def calculate_priority(
        self, 
        affected_users: int, 
        urgency: str
    ) -> str:
        if urgency == "high" and affected_users >= 10:
            return "critical"
        elif urgency == "high" or affected_users >= 10:
            return "high"
        elif urgency == "medium" or affected_users >= 3:
            return "medium"
        else:
            return "low"
    
    def list_tickets(self) -> str:
        if not self.data["tickets"]:
            return "There are no tickets right now. Please create one."
        tickets_str = ""
        for idx, ticket in enumerate(self.data["tickets"].values()):
            tickets_str += (
                f"{idx+1}  {ticket["id"]}  {ticket["title"]}\n"
            )
        return (
            "      Tickets List\n"
            "========================\n"
            f"{tickets_str}"
        )

    def assign_ticket(self, ticket_id: str, staff_name: str) -> None:
        require_non_empty(staff_name, "Staff name")
        require_non_empty(ticket_id, "Ticket ID")

        if ticket_id not in self.data["tickets"]:
            raise InvalidTicketIDError(f"Ticket '{ticket_id}' does not exist.")

        self.data["tickets"][ticket_id]["assigned_to"] = staff_name
    
    def work_queue(self) -> str:
        tickets = self.data["tickets"].values()

        open_tickets = [
            ticket
            for ticket in tickets
            if ticket["status"].lower() == "open"
        ]

        if not open_tickets:
            return "There are no open tickets in the work queue."

        sorted_tickets = sorted(
            open_tickets,
            key=lambda ticket: self.PRIORITY_ORDER[ticket["priority"].lower()]
        )

        queue_str = ""

        for idx, ticket in enumerate(sorted_tickets, start=1):
            queue_str += (
                f"{idx}. "
                f"{ticket['id']} | "
                f"{ticket['title']} | "
                f"{ticket['priority'].upper()}\n"
            )

        return (
            "          WORK QUEUE\n"
            "==============================\n"
            f"{queue_str}"
        )

    def update_ticket_status(
        self,
        ticket_id: str,
        new_status: TicketStatus
    ) -> None:
        if ticket_id not in self.data["tickets"]:
            raise InvalidTicketIDError("No ticket with this ID exists.")

        ticket = self.data["tickets"][ticket_id]
        current_status = ticket["status"]

        if current_status == TicketStatus.RESOLVED.value:
            # A resolved ticket can ONLY transition to OPEN
            if new_status != TicketStatus.OPEN:
                raise ValueError(
                    "Resolved tickets must be reopened before further changes."
                )

        elif current_status == TicketStatus.OPEN.value:
            # Open tickets can transition to IN_PROGRESS (if assigned) or stay OPEN
            if new_status == TicketStatus.IN_PROGRESS:
                if not ticket["assigned_to"]:
                    raise ValueError(
                        "An unassigned ticket cannot be moved into progress."
                    )
            elif new_status != TicketStatus.OPEN:
                # If it's not staying OPEN and it's not IN_PROGRESS, it's an invalid jump straight to RESOLVED
                raise ValueError(
                    f"Invalid transition: {current_status} → {new_status.value}."
                )

        elif current_status == TicketStatus.IN_PROGRESS.value:
            # In-progress tickets can ONLY transition to RESOLVED (or stay IN_PROGRESS)
            if new_status != TicketStatus.RESOLVED and new_status.value != current_status:
                raise ValueError(
                    f"Invalid transition: {current_status} → {new_status.value}."
                )

        else:
            raise ValueError(f"Unknown ticket status: {current_status}.")

        ticket["status"] = new_status.value

    def generate_report(self) -> str:
        tickets = self.data["tickets"].values()

        total_tickets = len(self.data["tickets"])

        status_counts = Counter(
            ticket["status"].lower()
            for ticket in tickets
        )

        priority_counts = Counter(
            ticket["priority"].lower()
            for ticket in tickets
        )

        report = (
            "          CAMPUSFLOW REPORT\n"
            "================================\n\n"
            f"TOTAL TICKETS: {total_tickets}\n\n"
            "TICKETS BY STATUS\n"
            "-----------------\n"
        )

        for status in TicketStatus:
            report += (
                f"{status.value.capitalize():<15}"
                f"{status_counts[status.value]}\n"
            )

        report += (
            "\nTICKETS BY PRIORITY\n"
            "-------------------\n"
        )

        for priority in ("critical", "high", "medium", "low"):
            report += (
                f"{priority.capitalize():<15}"
                f"{priority_counts[priority]}\n"
            )

        return report

    def view_ticket(self, ticket_id: str):
        if ticket_id not in self.data["tickets"]:
            raise InvalidTicketIDError("No ticket with this ID exists.")
        ticket: TicketDictType = self.data["tickets"][ticket_id]
        return (
            f"Ticket ID: {ticket["id"]}\n"
            f"Title: {ticket["title"]}\n"
            f"Category: {ticket["category"]}\n"
            f"Urgency: {ticket["urgency"].upper()}\n"
            f"Cases: {ticket["affected_users"]}\n"
            f"Priority: {ticket["priority"].upper()}\n"
            f"Status: {ticket["status"].capitalize()}\n"
            f"Assigned to: {ticket["assigned_to"]}\n"
        )

    def save(self) -> None:
        try:
            serialized_data: CampusFlowDict = {
                "tickets": {},
                "staff": {}
            }

            # 1. Fail-safe: Use safe get() fallback and ensure object attribute safety
            for id, ticket in self.data.get("tickets", {}).items():
                serialized_data["tickets"][id] = getattr(ticket, "__dict__", ticket)

            for id, staff in self.data.get("staff", {}).items():
                serialized_data["staff"][id] = getattr(staff, "__dict__", staff)

            # Ensure parent folder exists
            DB_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

            # 2. Fail-safe: Atomic write using a temporary file to prevent file corruption
            temp_file_path = DB_FILE_PATH.with_suffix(".tmp")
            
            with open(temp_file_path, 'w', encoding='utf-8') as file:
                json.dump(serialized_data, file, indent=4)
            
            # Atomically replace the old database file with the newly written one
            os.replace(temp_file_path, DB_FILE_PATH)
            print("Database successfully saved.")

        # 3. Fail-safe: Catch disk space, locked file, or system issues
        except (PermissionError, IOError) as e:
            raise DatabaseError(f"Failed to write database file.")

        except Exception as e:
            raise DatabaseError(f"An unexpected serialization error occurred during save: {e}")

    def load(self) -> None:
        if not os.path.exists(DB_FILE_PATH):
            print(f"Database file not found. Initializing empty data.")
            self.data = {
            "tickets": {},
            "staff": {}
        }
            return

        try:
            with open(DB_FILE_PATH, 'r', encoding='utf-8') as file:        
                self.data = json.load(file)
                
        except json.JSONDecodeError:
            print(f"Database file is corrupted or empty. Fallback to empty data.")
            self.data = {
            "tickets": {},
            "staff": {}
        }
            
        except PermissionError:
            print(f"Permission denied when trying to read database file.")
            self.data = {
            "tickets": {},
            "staff": {}
        }
            
        except Exception as e:
            print(f"Unexpected error loading database: {e}")
            self.data = {
            "tickets": {},
            "staff": {}
        }