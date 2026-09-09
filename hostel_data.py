# HK Hostel Data Setup

hostel_blocks = {
    "Block A": {
        "capacity_per_room": 4,
        "rooms": {
            "A101": [],
            "A102": [],
            "A103": [],
            "A104": []
        }
    },

    "Block B": {
        "capacity_per_room": 3,
        "rooms": {
            "B101": [],
            "B102": [],
            "B103": []
        }
    },

    "Block C": {
        "capacity_per_room": 2,
        "rooms": {
            "C101": [],
            "C102": [],
            "C103": [],
            "C104": []
        }
    }
}

print("HK HOSTEL DATA SETUP")
print("====================")

for block, data in hostel_blocks.items():
    print(block)
    print("Rooms:", len(data["rooms"]))
    print("Capacity per room:", data["capacity_per_room"])

print("\nHK HOSTEL OCCUPANCY OVERVIEW")
print("============================")

total_rooms = 0
total_capacity = 0
total_occupancy = 0

for block, data in hostel_blocks.items():
    rooms = data["rooms"]
    capacity = data["capacity_per_room"]

    block_capacity = len(rooms) * capacity
    block_occupancy = sum(len(students) for students in rooms.values())

    print(f"\n{block}")
    print("Rooms:", len(rooms))
    print("Capacity per room:", capacity)
    print("Total capacity:", block_capacity)
    print("Current occupancy:", block_occupancy)

    for room, students in rooms.items():
        print(f"  {room}: {len(students)}/{capacity} occupied")

    total_rooms += len(rooms)
    total_capacity += block_capacity
    total_occupancy += block_occupancy

print("\n----------------------------")
print("TOTAL BLOCKS:", len(hostel_blocks))
print("TOTAL ROOMS:", total_rooms)
print("TOTAL CAPACITY:", total_capacity)
print("CURRENT OCCUPANCY:", total_occupancy)
print("AVAILABLE SPACES:", total_capacity - total_occupancy)
print("============================")

# ==========================================
# STUDENT REGISTRATION AND ROOM ALLOCATION
# ==========================================

students = {}


def register_student():
    print("\nHK STUDENT REGISTRATION")
    print("=======================")

    # Get student details
    name = input("Enter student name: ").strip()
    registration_number = input("Enter registration number: ").strip().upper()

    # Validate empty inputs
    if name == "":
        print("Error: Student name cannot be empty.")
        return

    if registration_number == "":
        print("Error: Registration number cannot be empty.")
        return

    # Check whether student is already registered
    if registration_number in students:
        print("Error: Student is already registered.")
        return

    # Display hostel blocks
    print("\nAvailable Hostel Blocks:")
    for block in hostel_blocks:
        print("-", block)

    block = input("Enter hostel block: ").strip().title()

    # Check whether block exists
    if block not in hostel_blocks:
        print("Error: Hostel block does not exist.")
        return

    # Display rooms in selected block
    print(f"\nRooms available in {block}:")
    
    rooms = hostel_blocks[block]["rooms"]
    capacity = hostel_blocks[block]["capacity_per_room"]

    for room, occupants in rooms.items():
        print(f"{room}: {len(occupants)}/{capacity} occupied")

    # Select room
    room = input("Enter room number: ").strip().upper()

    # Check whether room exists
    if room not in rooms:
        print("Error: Room does not exist in this hostel block.")
        return

    # Check room capacity
    current_occupancy = len(rooms[room])

    if current_occupancy >= capacity:
        print(f"\nAllocation rejected.")
        print(
            f"Room {room} is already full "
            f"({current_occupancy}/{capacity})."
        )
        return

    # Add student to room
    rooms[room].append(registration_number)

    # Save student information
    students[registration_number] = {
        "name": name,
        "registration_number": registration_number,
        "block": block,
        "room": room
    }

    print("\nStudent registered successfully!")
    print("Student name:", name)
    print("Registration number:", registration_number)
    print("Hostel block:", block)
    print("Room:", room)

    print(
        f"Room occupancy: "
        f"{len(rooms[room])}/{capacity}")

