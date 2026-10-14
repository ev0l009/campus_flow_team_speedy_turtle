from campusflow.campusflow import CampusFlow

from campusflow.exceptions import InvalidAttributeError

from campusflow.ui import display_menu
from campusflow.ui import display_ticket_creation_menu

from campusflow.ui import category_menu, urgency_menu

from campusflow.exceptions import InvalidTicketIDError
from campusflow.exceptions import DatabaseError

campus_flow = CampusFlow()

CYAN = "\033[96m"
GRAY = "\033[90m"
RESET = "\033[0m"
GREEN = "\033[92m"

def campus_flow_runner():
    campus_flow.load()

    opt = "0"

    while opt != "7":

        if opt == "0":
            opt = input(display_menu())

        elif opt == "1":
            display_ticket_creation_menu()

            try:
                title = input(f"  {CYAN}📝 Ticket Title{RESET}       : ")
                category = input(category_menu)
                urgency = input(urgency_menu)
                users_affected = input(f"  {CYAN}👥 Users Affected{RESET}    : ")

                ticket_id = campus_flow.create_ticket(
                    title, 
                    category, 
                    urgency, 
                    users_affected
                )
                
            except InvalidAttributeError as err:
                print(f"\n  {GRAY}[Error]{RESET} {err}")
            else:
                print(f"\n  {GREEN}✔ Ticket with ID: {ticket_id} created successfully!{RESET}\n")

            opt = "0"

        elif opt == "2":
            print(campus_flow.list_tickets())

            opt = "0"

        elif opt == "3":
            ticket_id = input(f"  {CYAN}Enter your ticket ID{RESET}    : ")
            try:
                ticket = campus_flow.view_ticket(
                    ticket_id
                )
            except InvalidTicketIDError as err:
                print(err)
            else:
                print(ticket)

            opt = "0"

        elif opt == "4":
            print(f"\n{CYAN}--- ASSIGN STAFF ---{RESET}")
            ticket_id = input(f"  {CYAN}Enter ticket ID{RESET}    : ")
            staff_name = input(f"  {CYAN}Enter staff name{RESET} : ")

            try:
                campus_flow.assign_ticket(
                    ticket_id,
                    staff_name
                )
            except InvalidAttributeError as err:
                print(err)
            except InvalidTicketIDError as err:
                print(err)
            else:
                print(f"\n  {GREEN}✔ Ticket with ID: {ticket_id} successfully assigned to {staff_name}!{RESET}\n")

            opt = "0"

        elif opt == "5":
            print(campus_flow.work_queue())

            opt = "0"

        elif opt == "6":
            print(campus_flow.generate_report())

            opt = "0"

        elif opt not in ["1","2","3","4","5","6","7"]:
            print("Invalid selection. Try again...")

            opt = "0"

    try:
        campus_flow.save()
    except DatabaseError as err:
        print(err)
    else:
        print(f"\n  {GREEN}✔ Session saved{RESET}\n")

    print(f"\n{GREEN}Exiting{RESET}")

campus_flow_runner()