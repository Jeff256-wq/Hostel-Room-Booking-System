"""
GROUP 4 - HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM
Final integrated version
Antonio Sergio Mane - Main Menu, Integration, Final Debugging & Testing
"""

import json
import os

DATA_FILE = "hostel_data.json"

# INTEGRATION CHANGE: Original hostel_data.py used room occupant lists directly.
# I kept that simple structure because the room-allocation code also expects it.
DEFAULT_BLOCKS = {
    "Block A": {"capacity_per_room": 4, "rooms": {"A101": [], "A102": [], "A103": [], "A104": []}},
    "Block B": {"capacity_per_room": 3, "rooms": {"B101": [], "B102": [], "B103": []}},
    "Block C": {"capacity_per_room": 2, "rooms": {"C101": [], "C102": [], "C103": [], "C104": []}},
}


def fresh_data():
    """Return a new clean copy of the starting data."""
    return {
        "blocks": json.loads(json.dumps(DEFAULT_BLOCKS)),
        "students": {},
        "payments": []
    }


def save_data(data, filepath=DATA_FILE):
    """Save all shared system data to one JSON file."""
    temp_file = filepath + ".tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        os.replace(temp_file, filepath)
        return True
    except (OSError, TypeError) as error:
        print(f"Error: Data could not be saved ({error}).")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False


def load_data(filepath=DATA_FILE):
    """Load saved data and recover safely from a missing or damaged file."""
    # INTEGRATION CHANGE: Original persistence.py returned DEFAULT_DATA itself.
    # I return a fresh copy so later changes cannot accidentally modify the default.
    if not os.path.exists(filepath):
        print("No saved data file found. Starting with new hostel records.")
        data = fresh_data()
        save_data(data, filepath)
        return data

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # INTEGRATION CHANGE: Added a basic structure check before using loaded data.
        if not all(key in data for key in ("blocks", "students", "payments")):
            raise ValueError("required data sections are missing")

        print("Saved hostel data loaded successfully.")
        return data
    except (json.JSONDecodeError, ValueError, OSError) as error:
        print(f"Warning: Saved file is missing data or damaged ({error}).")
        print("The program will continue with fresh hostel records.")
        return fresh_data()


def get_valid_text(prompt):
    """Read required text without allowing a blank value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: This field cannot be empty.")


def get_valid_registration_number(students):
    """Read a unique registration number."""
    while True:
        reg_no = input("Enter registration number: ").strip().upper()
        if not reg_no:
            print("Error: Registration number is required.")
        elif reg_no in students:
            print("Error: This registration number already exists.")
        else:
            return reg_no


def get_valid_money(prompt, minimum=0, maximum=None):
    """Read a numeric money value inside the allowed range."""
    while True:
        try:
            value = float(input(prompt).strip().replace(",", ""))
            if value < minimum:
                print(f"Error: Amount must be at least {minimum:,.2f}.")
            elif maximum is not None and value > maximum:
                print(f"Error: Amount cannot exceed {maximum:,.2f}.")
            else:
                return value
        except ValueError:
            print("Error: Please enter a number.")


def occupancy_overview(blocks):
    """Print a brief occupancy overview when the program starts."""
    print("\n--- HOSTEL OCCUPANCY OVERVIEW ---")
    for block_name, block in blocks.items():
        capacity = block["capacity_per_room"]
        occupied = sum(len(room) for room in block["rooms"].values())
        total = len(block["rooms"]) * capacity
        print(f"{block_name}: {occupied}/{total} spaces occupied")


def register_student(students):
    """Register a student before room allocation."""
    print("\n--- STUDENT REGISTRATION ---")
    name = get_valid_text("Enter student's full name: ").title()
    reg_no = get_valid_registration_number(students)
    course = get_valid_text("Enter student's course: ").title()
    phone = get_valid_text("Enter phone number: ")
    total_fee = get_valid_money("Enter total hostel fee: ", minimum=1)

    # INTEGRATION CHANGE: Original student_registration.py used hostel_block/room_number,
    # while allocation/reports used block/room. I standardised them to block and room.
    students[reg_no] = {
        "registration_number": reg_no,
        "name": name,
        "course": course,
        "phone_number": phone,
        "total_fee": total_fee,
        "amount_paid": 0.0,
        "balance": total_fee,
        "block": None,
        "room": None,
        "payments": []
    }
    print(f"Student {name} ({reg_no}) registered successfully.")


def show_available_rooms(blocks):
    """Display blocks, rooms and current occupancy."""
    for block_name, block in blocks.items():
        capacity = block["capacity_per_room"]
        print(f"\n{block_name}")
        for room_no, occupants in block["rooms"].items():
            print(f"  {room_no}: {len(occupants)}/{capacity} occupied")


def allocate_student(students, blocks):
    """Allocate an already registered student if the selected room has space."""
    print("\n--- ROOM ALLOCATION ---")
    reg_no = input("Enter registration number: ").strip().upper()
    if reg_no not in students:
        print("Allocation rejected: Student is not registered.")
        return
    if students[reg_no]["room"] is not None:
        print(f"Allocation rejected: Student already has room {students[reg_no]['room']}.")
        return

    show_available_rooms(blocks)
    block_name = input("Enter hostel block: ").strip().title()
    if block_name not in blocks:
        print("Allocation rejected: Hostel block does not exist.")
        return

    room_no = input("Enter room number: ").strip().upper()
    rooms = blocks[block_name]["rooms"]
    if room_no not in rooms:
        print("Allocation rejected: Room does not exist in this block.")
        return

    capacity = blocks[block_name]["capacity_per_room"]
    if len(rooms[room_no]) >= capacity:
        print(f"Allocation rejected: {room_no} is already full.")
        return

    rooms[room_no].append(reg_no)
    students[reg_no]["block"] = block_name
    students[reg_no]["room"] = room_no
    print(f"Allocation successful: {reg_no} -> {block_name}/{room_no}.")


def record_payment(students, payments):
    """Record full or partial payment and update the same student's balance."""
    print("\n--- FEE PAYMENT ---")
    reg_no = input("Enter registration number: ").strip().upper()
    if reg_no not in students:
        print("Student not found.")
        return

    student = students[reg_no]
    outstanding = student["balance"]
    if outstanding <= 0:
        print("This student's fees are already fully paid.")
        return

    print(f"Student: {student['name']}")
    print(f"Outstanding balance: UGX {outstanding:,.2f}")
    payment = get_valid_money("Enter payment amount: ", minimum=0.01, maximum=outstanding)

    # INTEGRATION CHANGE: Original fees file updated outstanding_balance but reports
    # expected balance. I now update one shared balance field used by every module.
    student["amount_paid"] += payment
    student["balance"] = student["total_fee"] - student["amount_paid"]
    student["payments"].append(payment)

    # INTEGRATION CHANGE: Original persistence data had a payments list, while the fee
    # module only stored payment history inside the student. I update both records.
    payments.append({"registration_number": reg_no, "amount": payment})
    print(f"Payment recorded. New balance: UGX {student['balance']:,.2f}")


def search_student(students):
    """Search by registration number or exact student name."""
    print("\n--- STUDENT SEARCH ---")
    search = input("Enter student name or registration number: ").strip().lower()

    # INTEGRATION CHANGE: Original Nakafeero file used its own sample students list.
    # I changed search to use the live shared students dictionary from the final system.
    for reg_no, student in students.items():
        if reg_no.lower() == search or student["name"].lower() == search:
            print("Student Found")
            print(f"Name: {student['name']}")
            print(f"Registration Number: {reg_no}")
            print(f"Course: {student['course']}")
            print(f"Room: {student['block']} / {student['room']}")
            print(f"Total Fee: UGX {student['total_fee']:,.2f}")
            print(f"Paid: UGX {student['amount_paid']:,.2f}")
            print(f"Balance: UGX {student['balance']:,.2f}")
            return
    print("Student not found.")


def occupancy_report(blocks):
    """Generate a full occupancy report for every hostel block."""
    print("\n--- FULL OCCUPANCY REPORT ---")
    for block_name, block in blocks.items():
        capacity = block["capacity_per_room"]
        print(f"\n{block_name}")
        for room_no, occupants in block["rooms"].items():
            status = "FULL" if len(occupants) >= capacity else "AVAILABLE"
            print(f"{room_no}: {len(occupants)}/{capacity} occupied - {status}")


def fee_defaulters_report(students):
    """List students whose outstanding balance is above a chosen threshold."""
    threshold = get_valid_money("Enter outstanding-balance threshold: ", minimum=0)
    print(f"\n--- FEE DEFAULTERS ABOVE UGX {threshold:,.2f} ---")
    found = False
    for reg_no, student in students.items():
        if student["balance"] > threshold:
            found = True
            print(f"{reg_no} - {student['name']} - Balance: UGX {student['balance']:,.2f}")
    if not found:
        print("No fee defaulters above this threshold.")


def main():
    """Main menu that integrates all coursework requirements."""
    data = load_data()
    blocks = data["blocks"]
    students = data["students"]
    payments = data["payments"]

    occupancy_overview(blocks)

    while True:
        print("\n==============================================")
        print(" HOSTEL ROOM BOOKING & FEES MANAGEMENT SYSTEM")
        print("==============================================")
        print("1. Register Student")
        print("2. Allocate Room")
        print("3. Record Fee Payment")
        print("4. Search Student")
        print("5. Occupancy Report")
        print("6. Fee Defaulters Report")
        print("7. Save and Exit")

        choice = input("Choose an option (1-7): ").strip()

        # INTEGRATION CHANGE: Separate original files had independent menus/test blocks.
        # I replaced them with one looping driver menu so the warden uses one program.
        if choice == "1":
            register_student(students)
        elif choice == "2":
            allocate_student(students, blocks)
        elif choice == "3":
            record_payment(students, payments)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            occupancy_report(blocks)
        elif choice == "6":
            fee_defaulters_report(students)
        elif choice == "7":
            if save_data(data):
                print("All records saved. Program closed.")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
