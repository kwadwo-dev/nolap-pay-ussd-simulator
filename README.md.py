# nolap_pay.py
import time

# -------------------------------
# User Database (in-memory)
# -------------------------------
user_database = {
    "0200123456": {"pin": "1234", "balance": 150.75},
    "0500654321": {"pin": "9988", "balance": 45.00}
}
current_user_phone = None

# -------------------------------
# Helper Functions
# -------------------------------
def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def validate_pin(pin):
    return pin.isdigit() and len(pin) == 4

def input_pin(prompt="Enter PIN: "):
    pin = input(prompt)
    while not validate_pin(pin):
        print("Invalid PIN. Must be 4 digits.")
        pin = input(prompt)
    return pin

def display_balance(phone):
    print(f"Your balance is: GHS {user_database[phone]['balance']:.2f}")

def apply_fee(amount, rate, cap):
    fee = amount * rate
    return fee if fee < cap else cap

def pause():
    time.sleep(1)

# -------------------------------
# USSD Functions
# -------------------------------
def create_account():
    global current_user_phone
    phone = input("Enter your phone number (10 digits): ")
    while not validate_phone(phone) or phone in user_database:
        if phone in user_database:
            print("Number already exists. Try logging in.")
        else:
            print("Invalid phone number. Must be 10 digits.")
        phone = input("Enter your phone number: ")

    pin = input_pin("Create a 4-digit PIN: ")
    user_database[phone] = {"pin": pin, "balance": 0.0}
    current_user_phone = phone
    print("Account created successfully!")
    pause()
    main_menu()

def login():
    global current_user_phone
    phone = input("Enter your phone number: ")
    if phone not in user_database:
        print("Number not found. Please create an account.")
        create_account()
        return
    attempts = 3
    while attempts > 0:
        pin = input_pin()
        if pin == user_database[phone]["pin"]:
            current_user_phone = phone
            print("Login successful!")
            pause()
            main_menu()
            return
        else:
            attempts -= 1
            print(f"Incorrect PIN. Attempts left: {attempts}")
    print("Too many failed attempts. Exiting...")
    exit()

# -------------------------------
# Menu Functions
# -------------------------------
def transfer_money():
    recipient = input("Enter recipient phone number: ")
    if not validate_phone(recipient):
        print("Invalid phone number.")
        return
    if recipient not in user_database:
        print("Recipient does not exist.")
        return
    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print("Invalid amount.")
        return
    reference = input("Enter reference: ")
    fee = apply_fee(amount, 0.0075, 15)
    total = amount + fee
    print(f"Transfer fee: GHS {fee:.2f}")
    print(f"Total deducted: GHS {total:.2f}")
    pin = input_pin("Enter your PIN to confirm: ")
    if pin != user_database[current_user_phone]["pin"]:
        print("Incorrect PIN. Transaction cancelled.")
        return
    if user_database[current_user_phone]["balance"] < total:
        print("Insufficient funds.")
        return
    user_database[current_user_phone]["balance"] -= total
    user_database[recipient]["balance"] += amount
    print(f"Transferred GHS {amount:.2f} to {recipient} successfully!")

def buy_airtime():
    try:
        amount = float(input("Enter airtime amount: "))
    except ValueError:
        print("Invalid amount.")
        return
    pin = input_pin("Enter your PIN to confirm: ")
    if pin != user_database[current_user_phone]["pin"]:
        print("Incorrect PIN.")
        return
    if user_database[current_user_phone]["balance"] < amount:
        print("Insufficient funds.")
        return
    user_database[current_user_phone]["balance"] -= amount
    print(f"Airtime purchase of GHS {amount:.2f} successful!")

def withdraw_deposit():
    print("1. Withdraw\n2. Deposit")
    choice = input("Select option: ")
    if choice == "1":
        try:
            amount = float(input("Enter withdrawal amount: "))
        except ValueError:
            print("Invalid amount.")
            return
        fee = apply_fee(amount, 0.01, 20)
        total = amount + fee
        pin = input_pin("Enter PIN to confirm: ")
        if pin != user_database[current_user_phone]["pin"]:
            print("Incorrect PIN.")
            return
        if user_database[current_user_phone]["balance"] < total:
            print("Insufficient funds.")
            return
        user_database[current_user_phone]["balance"] -= total
        print(f"Withdrawal of GHS {amount:.2f} successful! Fee: GHS {fee:.2f}")
        print("Token: WDR12345")  # Simulated token
    elif choice == "2":
        try:
            amount = float(input("Enter deposit amount: "))
        except ValueError:
            print("Invalid amount.")
            return
        user_database[current_user_phone]["balance"] += amount
        print(f"Deposit of GHS {amount:.2f} successful!")
    else:
        print("Invalid option.")

def change_pin():
    old_pin = input_pin("Enter old PIN: ")
    if old_pin != user_database[current_user_phone]["pin"]:
        print("Incorrect old PIN.")
        return
    new_pin = input_pin("Enter new PIN: ")
    confirm = input_pin("Confirm new PIN: ")
    if new_pin != confirm:
        print("PINs do not match.")
        return
    user_database[current_user_phone]["pin"] = new_pin
    print("PIN changed successfully!")

# -------------------------------
# Main Menu
# -------------------------------
def main_menu():
    while True:
        print("\nWelcome to NOLAP Pay!")
        print("1. Transfer Money")
        print("2. Buy Airtime (Self)")
        print("3. Withdraw & Deposit")
        print("4. Check Balance")
        print("5. Change PIN")
        print("0. Exit")
        choice = input("Select option: ")
        if choice == "1":
            transfer_money()
        elif choice == "2":
            buy_airtime()
        elif choice == "3":
            withdraw_deposit()
        elif choice == "4":
            pin = input_pin()
            if pin == user_database[current_user_phone]["pin"]:
                display_balance(current_user_phone)
            else:
                print("Incorrect PIN.")
        elif choice == "5":
            change_pin()
        elif choice == "0":
            print("Thank you for using NOLAP Pay!")
            exit()
        else:
            print("Invalid option.")

# -------------------------------
# Entry Point
# -------------------------------
def main():
    print("Welcome to NOLAP Pay USSD Simulator")
    print("1. Login\n2. Create Account\n0. Exit")
    choice = input("Select option: ")
    if choice == "1":
        login()
    elif choice == "2":
        create_account()
    elif choice == "0":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice.")
        main()

if __name__ == "__main__":
    main()
