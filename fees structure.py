def record_payment(students):
    """Record a full or partial payment for a student."""

    print("\n--- Record Fee Payment ---")

    reg_no = input("Enter student registration number: ").strip()

    # Check whether the student exists
    if reg_no not in students:
        print("Student not found.")
        return

    student = students[reg_no]

    total_fees = student["total_fees"]
    amount_paid = student["amount_paid"]
    outstanding = total_fees - amount_paid

    print(f"\nStudent Name: {student['name']}")
    print(f"Registration Number: {reg_no}")
    print(f"Total Fees: {total_fees:,.2f}")
    print(f"Amount Already Paid: {amount_paid:,.2f}")
    print(f"Outstanding Balance: {outstanding:,.2f}")

    if outstanding <= 0:
        print("This student's fees are already fully paid.")
        return

    while True:
        try:
            payment = float(input("Enter payment amount: "))

            if payment <= 0:
                print("Payment must be greater than zero.")

            elif payment > outstanding:
                print(
                    f"Payment cannot exceed the outstanding balance "
                    f"of {outstanding:,.2f}."
                )

            else:
                break

        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Update amount paid
    student["amount_paid"] += payment

    # Calculate new outstanding balance
    student["outstanding_balance"] = (
        student["total_fees"] - student["amount_paid"]
    )

    # Store payment in payment history
    student["payments"].append(payment)

    print("\nPayment recorded successfully!")
    print(f"Payment Made: {payment:,.2f}")
    print(f"Total Amount Paid: {student['amount_paid']:,.2f}")
    print(f"Outstanding Balance: {student['outstanding_balance']:,.2f}")