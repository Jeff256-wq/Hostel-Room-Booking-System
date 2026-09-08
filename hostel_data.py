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