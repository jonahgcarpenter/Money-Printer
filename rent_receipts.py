from datetime import datetime

# Function to get bill details from user input
def get_monthly_bills():
    bills = {}
    print("Enter the details for each bill. Leave empty if there is no bill.")
    
    bills['Rent'] = float(input("Enter the Rent amount: ") or 0)
    bills['Internet'] = float(input("Enter the Internet bill: ") or 0)
    bills['Water'] = float(input("Enter the Water bill: ") or 0)
    bills['Electric'] = float(input("Enter the Electric bill: ") or 0)
    
    return bills

# Function to generate a receipt based on user-provided data
def generate_receipt(month_name, bills):
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Formatting the receipt
    receipt = f"Bill Receipt - {month_name}\n" + "-" * 30 + "\n"
    receipt += f"Date: {current_date}\n\n"
    for item, amount in bills.items():
        receipt += f"{item}: ${amount:.2f}\n"
    receipt += "-" * 30 + "\n"
    
    return receipt

# Main script to collect data for multiple months
def main():
    num_months = int(input("How many months of bills would you like to enter? "))
    all_receipts = []
    
    for i in range(num_months):
        month_name = input(f"\nEnter the month name for entry {i+1} (e.g., 'June 2024'): ")
        monthly_bills = get_monthly_bills()
        receipt = generate_receipt(month_name, monthly_bills)
        all_receipts.append(receipt)
    
    # Display all receipts
    for receipt in all_receipts:
        print(receipt)

# Run the main function
main()
