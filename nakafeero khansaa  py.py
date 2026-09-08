# Nakafeero Khansaa - Student Search and Reports

students = [
    {
        "name": "Sarah Nakato",
        "reg_no": "VU001",
        "room": "A101",
        "paid": 300000,
        "fees": 500000
    },
    {
        "name": "John Okello",
        "reg_no": "VU002",
        "room": "A102",
        "paid": 500000,
        "fees": 500000
    },
    {
        "name": "Mary Atim",
        "reg_no": "VU003",
        "room": "B101",
        "paid": 200000,
        "fees": 500000
    }
]

rooms = [
    {"room": "A101", "capacity": 4, "occupied": 3},
    {"room": "A102", "capacity": 4, "occupied": 4},
    {"room": "B101", "capacity": 3, "occupied": 1}
]


def search_student():
    search = input("Enter student name or registration number: ")

    for student in students:
        if (student["name"].lower() == search.lower()
                or student["reg_no"].lower() == search.lower()):
            print("\nStudent Found")
            print("Name:", student["name"])
            print("Registration Number:", student["reg_no"])
            print("Room:", student["room"])
            print("Fees:", student["fees"])
            print("Paid:", student["paid"])
            print("Balance:", student["fees"] - student["paid"])
            return

    print("Student not found.")


def occupancy_report():
    print("\n--- OCCUPANCY REPORT ---")

    for room in rooms:
        available = room["capacity"] - room["occupied"]

        print("Room:", room["room"])
        print("Capacity:", room["capacity"])
        print("Occupied:", room["occupied"])
        print("Available:", available)
        print()


def fee_defaulters_report():
    print("\n--- FEE DEFAULTERS REPORT ---")

    found = False

    for student in students:
        balance = student["fees"] - student["paid"]

        if balance > 0:
            found = True
            print("Name:", student["name"])
            print("Registration Number:", student["reg_no"])
            print("Balance:", balance)
            print()

    if not found:
        print("No fee defaulters found.")


# Main menu
while True:
    print("\n--- STUDENT SEARCH & REPORTS ---")
    print("1. Search Student")
    print("2. Occupancy Report")
    print("3. Fee Defaulters Report")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        search_student()
    elif choice == "2":
        occupancy_report()
    elif choice == "3":
        fee_defaulters_report()
    elif choice == "4":
        print("Program closed.")
        break
    else:
        print("Invalid choice. Please try again.")
