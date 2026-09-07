"""
input_validation.py
--------------------
Input Validation & Error Handling module
(Kilagga Alex's assigned part of the Hostel Room Booking and
Fees Management System group project)

Purpose
-------
This module centralises every piece of user-input checking used by the
rest of the system (registration, room allocation, fee payments,
search, reporting and the menu). Instead of each teammate writing their
own ad-hoc checks, they simply import and call these functions, so the
whole programme behaves consistently and never crashes on bad input.

How to use it in the rest of the group's code:

    from input_validation import (
        get_valid_menu_choice,
        get_valid_text,
        get_valid_registration_number,
        get_valid_integer,
        get_valid_float,
        get_yes_no,
        safe_int,
        safe_float,
    )
"""

# --------------------------------------------------------------------
# Low-level "safe conversion" helpers
# --------------------------------------------------------------------
# These never raise; they return None if conversion fails, so other
# modules (e.g. file loading) can check the result instead of wrapping
# every single conversion in their own try/except.

def safe_int(value):
    """Try to convert value to int. Return None instead of crashing."""
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return None


def safe_float(value):
    """Try to convert value to float. Return None instead of crashing."""
    try:
        return float(str(value).strip())
    except (ValueError, TypeError):
        return None


# --------------------------------------------------------------------
# Interactive validators — these DO the input() loop themselves and
# only return once the user has typed something acceptable.
# --------------------------------------------------------------------

def get_valid_text(prompt, allow_empty=False, max_length=60, letters_only=False):
    """
    Ask the user for a text value (e.g. student name, hostel block name)
    and keep asking until it is acceptable.

    - Strips leading/trailing spaces.
    - Rejects empty input unless allow_empty=True.
    - Rejects text longer than max_length characters.
    - If letters_only=True, allows letters, spaces, apostrophes and
      hyphens only (good for personal names like "Namata Gloria" or
      "O'Brien-Smith").
    """
    while True:
        try:
            value = input(prompt).strip()
        except EOFError:
            # Happens if input stream is closed / Ctrl+Z / Ctrl+D pressed.
            print("\nNo input received. Please try again.")
            continue

        if not value and not allow_empty:
            print("Error: This field cannot be empty. Please try again.")
            continue

        if len(value) > max_length:
            print(f"Error: Text is too long (max {max_length} characters). Please try again.")
            continue

        if letters_only and value:
            cleaned = value.replace(" ", "").replace("-", "").replace("'", "")
            if not cleaned.isalpha():
                print("Error: Please use letters only (spaces and hyphens allowed).")
                continue

        return value


def get_valid_registration_number(prompt, pattern_example="e.g. VU/2024/0123"):
    """
    Ask for a student registration number.
    Accepts alphanumeric characters plus '/' and '-' (covers formats like
    VU/2024/0123 or BC-S4-045). Rejects blanks and obviously wrong values.
    """
    while True:
        try:
            value = input(prompt).strip().upper()
        except EOFError:
            print("\nNo input received. Please try again.")
            continue

        if not value:
            print(f"Error: Registration number cannot be empty ({pattern_example}).")
            continue

        allowed_extra = {"/", "-"}
        if not all(ch.isalnum() or ch in allowed_extra for ch in value):
            print(f"Error: Registration number contains invalid characters ({pattern_example}).")
            continue

        if len(value) < 3:
            print("Error: Registration number looks too short. Please check and retype.")
            continue

        return value


def get_valid_integer(prompt, min_value=None, max_value=None):
    """
    Ask for a whole number (e.g. room number, capacity) and keep asking
    until the user supplies an integer within the optional min/max range.
    """
    while True:
        try:
            raw = input(prompt).strip()
        except EOFError:
            print("\nNo input received. Please try again.")
            continue

        value = safe_int(raw)
        if value is None:
            print("Error: Please enter a whole number (e.g. 12), not text or symbols.")
            continue

        if min_value is not None and value < min_value:
            print(f"Error: Value must be at least {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"Error: Value must not exceed {max_value}.")
            continue

        return value


def get_valid_float(prompt, min_value=0.0, max_value=None):
    """
    Ask for a decimal number (e.g. fee amount paid) and keep asking until
    it is a valid number within range. Defaults to rejecting negatives,
    since money paid can't sensibly be negative.
    """
    while True:
        try:
            raw = input(prompt).strip().replace(",", "")  # tolerate "150,000"
        except EOFError:
            print("\nNo input received. Please try again.")
            continue

        value = safe_float(raw)
        if value is None:
            print("Error: Please enter a numeric amount (e.g. 150000 or 150000.50).")
            continue

        if min_value is not None and value < min_value:
            print(f"Error: Amount cannot be less than {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"Error: Amount cannot exceed {max_value}.")
            continue

        return value


def get_valid_menu_choice(prompt, valid_choices):
    """
    Show a menu prompt and only accept one of the valid_choices
    (e.g. ["1", "2", "3", "4"]). Case-insensitive for letter menus.
    """
    valid_choices = [str(c).strip().upper() for c in valid_choices]
    while True:
        try:
            choice = input(prompt).strip().upper()
        except EOFError:
            print("\nNo input received. Please try again.")
            continue

        if choice not in valid_choices:
            print(f"Error: Invalid option. Please choose one of: {', '.join(valid_choices)}.")
            continue

        return choice


def get_yes_no(prompt):
    """Ask a yes/no question. Returns True for yes, False for no."""
    while True:
        try:
            choice = input(prompt + " (Y/N): ").strip().upper()
        except EOFError:
            print("\nNo input received. Please try again.")
            continue

        if choice in ("Y", "YES"):
            return True
        if choice in ("N", "NO"):
            return False

        print("Error: Please answer Y or N.")


# --------------------------------------------------------------------
# File-handling safety net (used by the persistence module, part e)
# --------------------------------------------------------------------

def safe_load_json(filepath, default_value):
    """
    Load a JSON file safely. If the file is missing, empty, or corrupted,
    print a friendly warning and return default_value instead of
    crashing the whole programme.
    """
    import json
    import os

    if not os.path.exists(filepath):
        print(f"Notice: '{filepath}' not found. Starting with a fresh, empty record.")
        return default_value

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"Notice: '{filepath}' is empty. Starting with a fresh, empty record.")
                return default_value
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Warning: '{filepath}' is damaged/corrupted and could not be read. "
              f"Starting with a fresh, empty record instead of crashing.")
        return default_value
    except (OSError, PermissionError) as e:
        print(f"Warning: Could not open '{filepath}' ({e}). Starting with a fresh, empty record.")
        return default_value


def safe_save_json(filepath, data):
    """
    Save data to a JSON file safely, reporting a clear message if saving
    fails (e.g. disk full, permission denied) instead of crashing.
    """
    import json

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except (OSError, PermissionError) as e:
        print(f"Error: Could not save to '{filepath}' ({e}). Your changes may be lost this session.")
        return False
