# HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM
# Student Registration Module
# Developed by: Odongkara Jefferson



def get_valid_name():
    """Request and validate the student's full name."""

    while True:
        name = input("Enter student's full name: ").strip()

        # Remove allowed spaces, hyphens and apostrophes
        name_check = name.replace(" ", "")
        name_check = name_check.replace("-", "")
        name_check = name_check.replace("'", "")

        if name == "":
            print("Error: Student name is required.")

        elif not name_check.isalpha():
            print("Error: Name should contain letters only.")

        else:
            return name.title()


def get_valid_registration_number(students):
    """Request and validate a unique registration number."""

    while True:
        registration_number = input(
            "Enter registration number: "
        ).strip().upper()

        if registration_number == "":
            print("Error: Registration number is required.")

        elif not registration_number.startswith("VU-"):
            print("Error: Registration number must start with 'VU-'.")

        elif registration_number in students:
            print(
                "Error: A student with this registration "
                "number already exists."
            )

        else:
            return registration_number


def get_valid_course():
    """Request and validate the student's course."""

    while True:
        course = input("Enter student's course: ").strip()

        if course == "":
            print("Error: Student course is required.")

        elif not course.replace(" ", "").isalpha():
            print("Error: Course must contain letters only.")

        else:
            return course.title()


def get_valid_phone_number():
    """Request and validate the student's phone number."""

    while True:
        phone_number = input("Enter phone number: ").strip()

        if phone_number == "":
            print("Error: Phone number is required.")

        elif not phone_number.isdigit():
            print("Error: Phone number must contain digits only.")

        elif len(phone_number) != 10:
            print("Error: Phone number must contain exactly 10 digits.")

        elif not phone_number.startswith("0"):
            print("Error: Phone number must start with 0.")

        else:
            return phone_number



def register_student(students):
    """Collect and register a new student's information."""

    print("\n===================================")
    print("       STUDENT REGISTRATION")
    print("===================================")

        # Collect the student's information
    name = get_valid_name()
    registration_number = get_valid_registration_number(students)
    course = get_valid_course()
    phone_number = get_valid_phone_number()
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

    while True:
        # Register one student
        register_student(students)

        # Ask whether another student should be registered
        another_student = input(
            "\nDo you want to register another student? (yes/no): "
        ).strip().lower()

        while another_student not in ["yes", "no"]:
            print("Error: Please enter yes or no.")
            another_student = input(
                "Do you want to register another student? (yes/no): "
            ).strip().lower()

        if another_student == "no":
            break

    # Display all saved students
    print("\n===================================")
    print("       REGISTERED STUDENTS")
    print("===================================")

    for registration_number, student in students.items():
        print(f"\nRegistration number: {registration_number}")
        print(f"Student name: {student['name']}")
        print(f"Course: {student['course']}")
        print(f"Phone number: {student['phone_number']}")

    print(f"\nTotal registered students: {len(students)}")
    print("Registration programme ended.")
