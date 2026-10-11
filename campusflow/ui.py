# Colors (ANSI escape codes)
CYAN = "\033[96m"
GREEN = "\033[92m"
GRAY = "\033[90m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[93m"

def display_menu():

    menu = f"""
{CYAN}{BOLD}  CAMPUS FLOW{RESET} {GRAY}— Support & Ticketing{RESET}
  {"─" * 38}

  {GREEN}1.{RESET} 📝  Create ticket
  {GREEN}2.{RESET} 📋  List tickets
  {GREEN}3.{RESET} 🔍  View ticket
  {GREEN}4.{RESET} 👤  Assign ticket
  {GREEN}5.{RESET} ⚡  Work queue
  {GREEN}6.{RESET} 📊  Reports

  {RED}7.{RESET} 🚪  Exit

  {CYAN}{BOLD}Select an option{RESET} {GRAY}[1-7]:{RESET}
"""
    return menu


def display_ticket_creation_menu():

    ticket_creation_menu_header = f"""
{CYAN}{BOLD}  CAMPUS FLOW{RESET} {GRAY}— Create Ticket{RESET}
  {"─" * 38}
  {GRAY}Please provide the details below:{RESET}
"""
    print(ticket_creation_menu_header)

category_menu = f"""
{CYAN}{BOLD}  CAMPUS FLOW{RESET} {GRAY}— Select Category{RESET}
  {"─" * 38}

  {GREEN}1.{RESET} 🌐  Network
  {GREEN}2.{RESET} 💻  Hardware
  {GREEN}3.{RESET} 📦  Software
  {GREEN}4.{RESET} 💬  Other
"""

urgency_menu = f"""
{CYAN}{BOLD}  CAMPUS FLOW{RESET} {GRAY}— Urgency Level{RESET}
  {"─" * 38}

  {RED}1.{RESET} 🔴  High
  {YELLOW}2.{RESET} 🟡  Medium
  {GREEN}3.{RESET} 🟢  Low
"""