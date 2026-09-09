import json
import os

DATA_FILE = "hostel_data.json"

DEFAULT_DATA = {
    "blocks": {
        "Block A": {"rooms": {"A101": {"capacity": 2, "occupants": []}, "A102": {"capacity": 2, "occupants": []}}},
        "Block B": {"rooms": {"B201": {"capacity": 3, "occupants": []}, "B202": {"capacity": 3, "occupants": []}}},
        "Block C": {"rooms": {"C301": {"capacity": 2, "occupants": []}, "C302": {"capacity": 2, "occupants": []}}}
    },
    "students": {},
    "payments": []
}

def load_data(filepath=DATA_FILE):
    """Loads system data safely; handles missing/corrupt files without crashing."""
    if not os.path.exists(filepath):
        print(f"[Notice] File '{filepath}' not found. Initializing new database with defaults.")
        save_data(DEFAULT_DATA, filepath)
        return DEFAULT_DATA

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            print(f"[Success] Data loaded successfully from '{filepath}'.")
            return data
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[Warning] Data file corrupted: {e}")
        print("[Recovery] Backing up broken file and restoring default state.")
        backup_corrupt_file(filepath)
        save_data(DEFAULT_DATA, filepath)
        return DEFAULT_DATA

def save_data(data, filepath=DATA_FILE):
    """Saves data safely using atomic write operations."""
    temp_filepath = filepath + ".tmp"
    try:
        with open(temp_filepath, 'w') as file:
            json.dump(data, file, indent=4)
        
        if os.path.exists(filepath):
            os.replace(temp_filepath, filepath)
        else:
            os.rename(temp_filepath, filepath)
            
        print(f"[Success] State saved to '{filepath}'.")
        return True
    except Exception as e:
        print(f"[Error] Save failed: {e}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return False

def backup_corrupt_file(filepath):
    """Preserves damaged files for manual inspection."""
    corrupt_backup = filepath + ".corrupt.bak"
    try:
        if os.path.exists(filepath):
            os.replace(filepath, corrupt_backup)
            print(f"[Backup] Corrupt file moved to '{corrupt_backup}'.")
    except Exception as e:
        print(f"[Warning] Could not back up corrupt file: {e}")
        