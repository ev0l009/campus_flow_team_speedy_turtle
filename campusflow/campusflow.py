from pathlib import Path
import json

import os

from utils.helpers import generate_prefixed_id

from utils.validators import require_non_empty, check_affected_users, get_category, get_urgency

from campusflow.exceptions import InvalidTicketIDError, DatabaseError

from collections import Counter

from campusflow.types import TicketDictType, TicketStatus, Urgency

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
        self.tickets: dict[str, TicketDictType] = {}

    def create_ticket(
        self, 
        title: str, 
        category: str, 
        urgency: str, 
        affected_users: str
    ) -> str:
        require_non_empty(title, "Title")
        validated_category = get_category(category)
        validated_urgency = get_urgency(urgency)
        validated_cases = check_affected_users(affected_users)
 
        ticket_id = generate_prefixed_id("tkt")

        self.tickets[ticket_id]  = {
            "id": ticket_id,
            "title": title,
            "category": validated_category,
            "urgency": validated_urgency,
            "affected_users": validated_cases,
            "priority": self.calculate_priority(validated_cases, validated_urgency),
            "status": TicketStatus.OPEN.value,
            "assigned_to": None   
        }

        return ticket_id

    def calculate_priority(
        self, 
        affected_users: int, 
        urgency: str
    ) -> str:
        if urgency == Urgency.HIGH.value and affected_users >= 10:
            return "critical"
        elif urgency == Urgency.HIGH.value or affected_users >= 10:
            return "high"
        elif urgency == Urgency.MEDIUM.value or affected_users >= 3:
            return "medium"
        else:
            return "low"
    
    def list_tickets(self) -> str:
        if not self.tickets:
            return "There are no tickets right now. Please create one."
        
        tickets_str = ""
        for idx, ticket in enumerate(self.tickets.values()):
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

        if ticket_id not in self.tickets:
            raise InvalidTicketIDError(f"Ticket '{ticket_id}' does not exist.")

        self.tickets[ticket_id]["assigned_to"] = staff_name
    
    def work_queue(self) -> str:
        tickets = self.tickets.values()

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

    def generate_report(self) -> str:
        tickets = self.tickets.values()

        total_tickets = len(self.tickets)

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
        if ticket_id not in self.tickets:
            raise InvalidTicketIDError("No ticket with this ID exists.")
        ticket: TicketDictType = self.tickets[ticket_id]
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
            DB_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

            temp_file_path = DB_FILE_PATH.with_suffix(".tmp")
            
            with open(temp_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.tickets, file, indent=4)
            
            os.replace(temp_file_path, DB_FILE_PATH)

        except (PermissionError, IOError) as e:
            raise DatabaseError(f"Error: {e}")

        except Exception as e:
            raise DatabaseError(f"An error occurred during save: {e}")

    def load(self) -> None:
        if not os.path.exists(DB_FILE_PATH):
            print(f"Database file not found. Initializing empty data.")
            self.tickets = {}
            return

        try:
            with open(DB_FILE_PATH, 'r', encoding='utf-8') as file:        
                self.data = json.load(file)
                
        except json.JSONDecodeError:
            print(f"Database file is corrupted or empty. Fallback to empty data.")
            self.tickets = {}
            
        except PermissionError:
            print(f"Permission denied when trying to read database file.")
            self.tickets = {}
            
        except Exception as e:
            print(f"Unexpected error loading database: {e}")
            self.tickets = {}