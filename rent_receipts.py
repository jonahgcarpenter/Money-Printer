from datetime import datetime

# Function to get expense details from user input with numeric validation
def get_monthly_expenses():
    rent = {}
    bills = {}
    print("Enter the details for each expense. Leave empty if there is no cost for that item.")
    
    # Function to get a valid numeric input
    def get_numeric_input(prompt):
        while True:
            try:
                value = input(prompt)
                if value == "":
                    return 0.0
                return float(value)
            except ValueError:
                print("Please enter a valid number.")

    # Collecting rent and other bill amounts with validation
    rent['Rent'] = get_numeric_input("Enter the Rent amount: ")
    bills['Internet'] = get_numeric_input("Enter the Internet bill: ")
    bills['Water'] = get_numeric_input("Enter the Water bill: ")
    bills['Electric'] = get_numeric_input("Enter the Electric bill: ")
    
    return rent, bills

# Function to calculate each roommate's share based on provided logic
def calculate_shares(rent, bills):
    # Calculate total expenses for the month
    rent_cost = rent.get('Rent', 0)
    utilities = sum(bills.values())
    total_expenses = rent_cost + utilities
    
    # Calculate roommates' share as 2/3 of the total expenses
    roommates_share = (2 / 3) * total_expenses
    
    # Calculate Jonah's rent share
    jonah_share_rent = rent_cost - roommates_share
    
    # Jonah's utility share (all bills)
    jonah_share_util = utilities
    
    # Total share for Jonah
    jonah_share_total = jonah_share_rent + jonah_share_util
    
    # Grant and Will's shares (half of roommates_share each)
    grant_share = roommates_share / 2
    will_share = roommates_share / 2
    
    return total_expenses, jonah_share_rent, jonah_share_util, jonah_share_total, grant_share, will_share, roommates_share, rent_cost

# Function to generate a receipt based on user-provided data
def generate_receipt(rent, bills):
    # Automatically determine the current month and year
    month_name = datetime.now().strftime("%B %Y")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Calculate shares
    total_expenses, jonah_share_rent, jonah_share_util, jonah_share_total, grant_share, will_share, roommates_share, rent_cost = calculate_shares(rent, bills)
    
    # Formatting the receipt
    receipt = f"Bill Receipt - {month_name}\n" + "-" * 30 + "\n"
    receipt += f"Date: {current_date}\n\n"
    
    # Display rent
    receipt += f"Rent: ${rent.get('Rent', 0):.2f}\n"
    
    # Display individual bills
    for item, amount in bills.items():
        receipt += f"{item}: ${amount:.2f}\n"
    
    # Display the total expenses and roommate shares
    receipt += "\nTotal Expenses: ${:.2f}\n".format(total_expenses)
    receipt += f"Roommates' Total Share (2/3 of Total): ${roommates_share:.2f}\n"
    receipt += "-" * 30 + "\n"
    receipt += "Roommate Contributions:\n"
    receipt += f"Grant's Share: ${grant_share:.2f}\n"
    receipt += f"Will's Share: ${will_share:.2f}\n"
    receipt += f"Jonah's Share:\n  Total: ${jonah_share_total:.2f}\n  + Rent: ${jonah_share_rent:.2f}\n  + Utilities: ${jonah_share_util:.2f}\n"
    receipt += "-" * 30 + "\n"
    
    # Double Checking Section
    receipt += "Double Checking:\n"
    receipt += f"Roommates' Share + Jonah's Rent Share = Total Rent\n"
    receipt += f"${roommates_share:.2f} + ${jonah_share_rent:.2f} = ${rent_cost:.2f}\n"
    receipt += "-" * 30 + "\n"
    
    return receipt

# Main script to collect data for one month
def main():
    rent, bills = get_monthly_expenses()
    receipt = generate_receipt(rent, bills)
    
    # Display the receipt
    print(receipt)

# Run the main function
main()
