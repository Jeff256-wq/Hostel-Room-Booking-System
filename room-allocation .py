"""
====================================================================
HOSTEL ROOM BOOKING SYSTEM
Part 7: Room Allocation & Occupancy Update
Author: Kiconco Rosette
====================================================================

INTEGRATION NOTE (read this first)
-----------------------------------
Kenneth's hostel_data.py already contains hostel_blocks + a
register_student() function that ALSO does room allocation inline
(it asks for a block/room and appends the reg number itself).

That overlaps with my assigned part. To avoid two different pieces
of allocation logic in the final system, this module is written to
use the EXACT same data structures Kenneth built:

    hostel_blocks = {
        "Block A": {
            "capacity_per_room": 4,
            "rooms": {
                "A101": [ "reg_no", ... ],   # list of occupant reg numbers
                ...
            }
        },
        ...
    }

    students = {
        "reg_no": {
            "name": "...",
            "registration_number": "...",
            "block": "Block A" or None,
            "room": "A101" or None
        },
        ...
    }

WHAT I'M ADDING THAT DOESN'T ALREADY EXIST
--------------------------------------------
1. allocate_student() - allocate an already-registered student who
   has NOT yet been given a room (e.g. registered without picking
   one, or Antonio wants allocation kept separate from registration
   during integration).
2. transfer_student() - move a student who already has a room to a
   different room (frees the old room, fills the new one). This did
   not exist anywhere else in the repo.
3. occupancy_report() - a reusable version of the occupancy printout,
   so Fred's reports module can call it directly instead of copying
   the print logic.

SUGGESTION FOR ANTONIO (integration):
   Either (a) have register_student() call allocate_student() below
   instead of repeating the block/room logic inline, or (b) keep
   register_student() as "registration only" and require every
   student to go through allocate_student() afterwards. Either way,
   only one piece of code should be deciding "is this room full?".
"""


# ------------------------------------------------------------------
# SAMPLE DATA - matches Kenneth's hostel_data.py exactly, used only
# to test this module on its own. Replace with the real imported
# hostel_blocks / students dictionaries at integration time.
# ------------------------------------------------------------------
hostel_blocks = {
    "Block A": {
        "capacity_per_room": 4,
        "rooms": {
            "A101": [],
            "A102": [],
        }
    },
    "Block B": {
        "capacity_per_room": 2,
        "rooms": {
            "B101": [],
        }
    },
}

students = {
    "S001": {"name": "Alice Namu", "registration_number": "S001",
              "block": None, "room": None},
    "S002": {"name": "Brian Okot", "registration_number": "S002",
              "block": None, "room": None},
    "S003": {"name": "Cynthia Aber", "registration_number": "S003",
              "block": None, "room": None},
    "S004": {"name": "David Ouma", "registration_number": "S004",
              "block": None, "room": None},
}


# ------------------------------------------------------------------
# CORE FUNCTION: allocate a registered student to a room
# ------------------------------------------------------------------
def allocate_student(reg_no, block_name, room_no, hostel_blocks, students):
    """
    Allocates student `reg_no` to `room_no` inside `block_name`.
    Returns (success: bool, message: str)
    """

    # 1. Student must be registered
    if reg_no not in students:
        return False, f"REJECTED: Student '{reg_no}' is not registered."

    # 2. Student must not already have a room
    if students[reg_no]["room"] is not None:
        return False, (f"REJECTED: Student '{reg_no}' already has room "
                        f"'{students[reg_no]['room']}' in "
                        f"'{students[reg_no]['block']}'. Use "
                        f"transfer_student() to move them instead.")

    # 3. Block must exist
    if block_name not in hostel_blocks:
        return False, f"REJECTED: Hostel block '{block_name}' does not exist."

    block = hostel_blocks[block_name]
    rooms = block["rooms"]
    capacity = block["capacity_per_room"]

    # 4. Room must exist in that block
    if room_no not in rooms:
        return False, (f"REJECTED: Room '{room_no}' does not exist in "
                        f"'{block_name}'.")

    # 5. Room must not be full
    occupants = rooms[room_no]
    if len(occupants) >= capacity:
        return False, (f"REJECTED: Room '{room_no}' in '{block_name}' is "
                        f"full ({len(occupants)}/{capacity}).")

    # 6. All checks passed -> allocate
    occupants.append(reg_no)
    students[reg_no]["block"] = block_name
    students[reg_no]["room"] = room_no
    return True, (f"ACCEPTED: {students[reg_no]['name']} ({reg_no}) "
                   f"allocated to {block_name} / {room_no}. "
                   f"Room now {len(occupants)}/{capacity}.")


# ------------------------------------------------------------------
# Move a student who already has a room into a different room
# ------------------------------------------------------------------
def transfer_student(reg_no, new_block, new_room, hostel_blocks, students):
    """
    Moves an already-allocated student to a new room.
    Returns (success: bool, message: str)
    """
    if reg_no not in students or students[reg_no]["room"] is None:
        return False, (f"REJECTED: Student '{reg_no}' has no current room "
                        f"to transfer from. Use allocate_student() instead.")

    old_block = students[reg_no]["block"]
    old_room = students[reg_no]["room"]

    if new_block not in hostel_blocks:
        return False, f"REJECTED: Hostel block '{new_block}' does not exist."
    new_rooms = hostel_blocks[new_block]["rooms"]
    new_capacity = hostel_blocks[new_block]["capacity_per_room"]

    if new_room not in new_rooms:
        return False, f"REJECTED: Room '{new_room}' does not exist in '{new_block}'."

    if len(new_rooms[new_room]) >= new_capacity:
        return False, (f"REJECTED: Room '{new_room}' in '{new_block}' is full "
                        f"({len(new_rooms[new_room])}/{new_capacity}).")

    # Free the old room, fill the new one
    hostel_blocks[old_block]["rooms"][old_room].remove(reg_no)
    new_rooms[new_room].append(reg_no)
    students[reg_no]["block"] = new_block
    students[reg_no]["room"] = new_room

    return True, (f"UPDATED: {students[reg_no]['name']} ({reg_no}) moved "
                   f"from {old_block}/{old_room} to {new_block}/{new_room}.")


# ------------------------------------------------------------------
# Free a student's room entirely (e.g. they leave the hostel)
# ------------------------------------------------------------------
def remove_student_from_room(reg_no, hostel_blocks, students):
    if reg_no not in students or students[reg_no]["room"] is None:
        return False, f"REJECTED: Student '{reg_no}' has no room to remove."

    block_name = students[reg_no]["block"]
    room_no = students[reg_no]["room"]
    hostel_blocks[block_name]["rooms"][room_no].remove(reg_no)
    students[reg_no]["block"] = None
    students[reg_no]["room"] = None
    return True, f"UPDATED: {reg_no} removed from {block_name}/{room_no}."


# ------------------------------------------------------------------
# Reusable occupancy report (Fred's reports module can call this)
# ------------------------------------------------------------------
def occupancy_report(hostel_blocks):
    lines = []
    total_rooms = total_capacity = total_occupancy = 0
    for block_name, data in hostel_blocks.items():
        capacity = data["capacity_per_room"]
        rooms = data["rooms"]
        lines.append(f"\n{block_name}")
        for room_no, occupants in rooms.items():
            lines.append(f"  {room_no}: {len(occupants)}/{capacity} occupied -> {occupants}")
            total_rooms += 1
            total_capacity += capacity
            total_occupancy += len(occupants)
    lines.append("\n----------------------------")
    lines.append(f"TOTAL ROOMS: {total_rooms}")
    lines.append(f"TOTAL CAPACITY: {total_capacity}")
    lines.append(f"CURRENT OCCUPANCY: {total_occupancy}")
    lines.append(f"AVAILABLE SPACES: {total_capacity - total_occupancy}")
    return "\n".join(lines)


# ------------------------------------------------------------------
# DEMO / TEST RUN - screenshot this for accepted & rejected examples
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("ROOM ALLOCATION TEST RESULTS")
    print("=" * 40)

    test_cases = [
        ("S001", "Block A", "A101"),   # accepted
        ("S002", "Block A", "A101"),   # accepted
        ("S003", "Block B", "B101"),   # accepted -> B101 now full
        ("S004", "Block B", "B101"),   # rejected -> room full
        ("S999", "Block A", "A102"),   # rejected -> student not registered
        ("S001", "Block A", "A102"),   # rejected -> already has a room
        ("S004", "Block Z", "Z1"),     # rejected -> block doesn't exist
    ]

    for reg_no, block_name, room_no in test_cases:
        success, message = allocate_student(reg_no, block_name, room_no,
                                             hostel_blocks, students)
        print(message)

    print(occupancy_report(hostel_blocks))

    print("\nTesting transfer:")
    success, message = transfer_student("S001", "Block A", "A102",
                                         hostel_blocks, students)
    print(message)

    print("\nTesting removal:")
    success, message = remove_student_from_room("S002", hostel_blocks, students)
    print(message)

    print(occupancy_report(hostel_blocks))
