# HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM
# Student Registration Module
# Developed by: Odongkara Jefferson


def register_student(students):
    """Collect and register a new student's information."""

    print("\n===================================")
    print("       STUDENT REGISTRATION")
    print("===================================")

    # Collect the student's information
    name = input("Enter student's full name: ").strip()
    registration_number = input(
        "Enter registration number: "
    ).strip().upper()
    course = input("Enter student's course: ").strip()
    phone_number = input("Enter phone number: ").strip()
    # Request and validate the total hostel fee
    while True:
        fee_input = input("Enter total hostel fee: ").strip()

        try:
            total_fee = int(fee_input)

            if total_fee > 0:
                break

            print("Error: Total hostel fee must be greater than zero.")

        except ValueError:
            print("Error: Enter the hostel fee using numbers only.")

    # Create a dictionary containing the student's information
    student_record = {
        "registration_number": registration_number,
        "name": name,
        "course": course,
        "phone_number": phone_number,
        "total_fee": total_fee,
        "amount_paid": 0,
        "balance": total_fee,
        "hostel_block": None,
        "room_number": None
    }

    # Store the record in the shared students dictionary
    students[registration_number] = student_record

    print("\nStudent registered successfully!")
    print(f"Registration number: {registration_number}")
    print(f"Student name: {name}")
    print(f"Course: {course}")
    print(f"Phone number: {phone_number}")
    print(f"Total hostel fee: UGX {total_fee:,}")
    print(f"Outstanding balance: UGX {total_fee:,}")
    print("Hostel room: Not yet allocated")

    return student_record
# Run this section only when testing this file directly
if __name__ == "__main__":

    # Create an empty dictionary for storing students
    students = {}

    print("HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM")

    # Call the registration function
    register_student(students)

    # Display the dictionary to confirm that the record was stored
    print("\nSaved student record:")
    print(students)
