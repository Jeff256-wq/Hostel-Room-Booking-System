# reports.py
# Occupancy report and fee-defaulters report

# students dict is as:
# students = {
#     "REG001": {"name": "Abesiga Sam", "block": "Block A", "room": "A101",
#                 "total_fee": 1500000, "paid": 500000, "balance": 1000000}
# }

# blocks dict looks like this:
# blocks = {
#     "Block A": {"rooms": {"A101": {"capacity": 4, "occupants": ["REG001", "REG002"]}}}
# }


def block_occupancy_report(blocks):
    report = ""
    report += "HOSTEL OCCUPANCY REPORT\n"
    report += "=" * 50 + "\n"

    total_capacity = 0
    total_occupied = 0

    for block_name in blocks:
        rooms = blocks[block_name]["rooms"]
        block_capacity = 0
        block_occupied = 0

        report += "\n" + block_name + "\n"
        report += "Room       Occupied   Capacity   Status\n"

        for room_no in sorted(rooms):
            room = rooms[room_no]
            capacity = room.get("capacity", 0)
            occupants = room.get("occupants", [])
            occupied = len(occupants)

            if occupied >= capacity:
                status = "FULL"
            elif occupied == 0:
                status = "EMPTY"
            else:
                status = "AVAILABLE"

            report += f"{room_no:<10} {occupied:<10} {capacity:<10} {status}\n"

            block_capacity += capacity
            block_occupied += occupied

        if block_capacity > 0:
            pct = block_occupied / block_capacity * 100
        else:
            pct = 0
        report += f"Block total: {block_occupied}/{block_capacity} occupied ({pct:.1f}%)\n"

        total_capacity += block_capacity
        total_occupied += block_occupied

    if total_capacity > 0:
        overall_pct = total_occupied / total_capacity * 100
    else:
        overall_pct = 0

    report += "\n" + "=" * 50 + "\n"
    report += f"OVERALL: {total_occupied}/{total_capacity} occupied ({overall_pct:.1f}%)\n"

    return report


def fee_defaulters_report(students, threshold):
    defaulters = []
    for reg_no in students:
        record = students[reg_no]
        if record.get("balance", 0) > threshold:
            record["reg_no"] = reg_no
            defaulters.append(record)

    # sort highest balance first
    defaulters.sort(key=lambda x: x.get("balance", 0), reverse=True)
    return defaulters


def print_defaulters(defaulters, threshold):
    print(f"\nFEE DEFAULTERS (balance above {threshold})")
    print("-" * 50)

    if not defaulters:
        print("No defaulters above this threshold.")
        return

    for d in defaulters:
        print(d.get("reg_no"), "-", d.get("name"), "-", d.get("block"), "/", d.get("room"),
              "- balance:", d.get("balance", 0))


def get_threshold_from_user():
    # asks the warden for a balance threshold and keeps asking until
    # they type something usable
    while True:
        value = input("Enter balance threshold for defaulters report: ").strip()
        try:
            threshold = float(value)
        except ValueError:
            print("That's not a number, try again.")
            continue

        if threshold < 0:
            print("Threshold can't be negative, try again.")
            continue

        return threshold


def run_occupancy_report(blocks):
    # called from the main menu
    print(block_occupancy_report(blocks))


def run_defaulters_report(students):
    # called from the main menu
    threshold = get_threshold_from_user()
    defaulters = fee_defaulters_report(students, threshold)
    print_defaulters(defaulters, threshold)


if __name__ == "__main__":
    # quick test data just to check the functions work
    blocks = {
        "Block A": {"rooms": {
            "A101": {"capacity": 4, "occupants": ["REG001", "REG002"]},
            "A102": {"capacity": 4, "occupants": []},
        }},
        "Block B": {"rooms": {
            "B201": {"capacity": 2, "occupants": ["REG003", "REG004"]},
        }},
        "Block C": {"rooms": {
            "C301": {"capacity": 3, "occupants": ["REG005"]},
        }},
    }

    students = {
        "REG001": {"name": "Abesiga Sam", "block": "Block A", "room": "A101",
                   "total_fee": 1500000, "paid": 500000, "balance": 1000000},
        "REG002": {"name": "Aine Adolf", "block": "Block A", "room": "A101",
                   "total_fee": 1500000, "paid": 1500000, "balance": 0},
        "REG003": {"name": "Wambi Kato", "block": "Block B", "room": "B201",
                   "total_fee": 1200000, "paid": 200000, "balance": 1000000},
        "REG004": {"name": "Phillip Okello", "block": "Block B", "room": "B201",
                   "total_fee": 1200000, "paid": 1200000, "balance": 0},
        "REG005": {"name": "Daisy Esther", "block": "Block C", "room": "C301",
                   "total_fee": 1000000, "paid": 100000, "balance": 900000},
    }

    print(block_occupancy_report(blocks))
    print_defaulters(fee_defaulters_report(students, 500000), 500000)
