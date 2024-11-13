from datetime import datetime
from tkinter import Tk, Label, Entry, Button, Text, END
from tkinter.filedialog import asksaveasfilename
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# Function to calculate each roommate's share based on provided logic
def calculate_shares(rent, bills):
    rent_cost = rent.get('Rent', 0)
    utilities = sum(bills.values())
    total_expenses = rent_cost + utilities
    
    roommates_share = (2 / 3) * total_expenses
    jonah_share_rent = rent_cost - roommates_share
    jonah_share_util = utilities
    jonah_share_total = jonah_share_rent + jonah_share_util
    grant_share = roommates_share / 2
    will_share = roommates_share / 2
    
    return total_expenses, jonah_share_rent, jonah_share_util, jonah_share_total, grant_share, will_share, roommates_share, rent_cost

# Function to generate receipt text
def generate_receipt_text(rent, bills):
    total_expenses, jonah_share_rent, jonah_share_util, jonah_share_total, grant_share, will_share, roommates_share, rent_cost = calculate_shares(rent, bills)
    
    # Create receipt text similar to the console output
    receipt = f"Bill Receipt - {datetime.now().strftime('%B %Y')}\n" + "-" * 30 + "\n"
    receipt += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    receipt += f"Rent: ${rent.get('Rent', 0):.2f}\n"
    
    for item, amount in bills.items():
        receipt += f"{item}: ${amount:.2f}\n"
    
    receipt += "\nTotal Expenses: ${:.2f}\n".format(total_expenses)
    receipt += f"Roommates' Total Share (2/3 of Total): ${roommates_share:.2f}\n"
    receipt += "-" * 30 + "\n"
    receipt += "Roommate Contributions:\n"
    receipt += f"Grant's Share: ${grant_share:.2f}\n"
    receipt += f"Will's Share: ${will_share:.2f}\n"
    receipt += f"Jonah's Share:\n  Total: ${jonah_share_total:.2f}\n  + Rent: ${jonah_share_rent:.2f}\n  + Utilities: ${jonah_share_util:.2f}\n"
    receipt += "-" * 30 + "\n"
    receipt += "Double Checking:\n"
    receipt += f"Roommates' Share + Jonah's Rent Share = Total Rent\n"
    receipt += f"${roommates_share:.2f} + ${jonah_share_rent:.2f} = ${rent_cost:.2f}\n"
    receipt += "-" * 30 + "\n"
    
    return receipt

# Function to save the receipt as a PDF, prompting for location
def save_pdf(receipt_text):
    # Generate the default filename based on the current month and year
    default_filename = f"{datetime.now().strftime('%B %Y')} Rent Receipt.pdf"
    
    # Prompt the user to choose where to save the PDF with the default filename
    file_path = asksaveasfilename(defaultextension=".pdf", 
                                  filetypes=[("PDF files", "*.pdf")], 
                                  title="Save as PDF", 
                                  initialfile=default_filename)
    
    # Proceed only if a path was chosen
    if file_path:
        pdf_buffer = io.BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4
        y = height - 50
        
        p.setFont("Helvetica", 12)
        for line in receipt_text.splitlines():
            p.drawString(100, y, line)
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica", 12)
        
        p.save()
        
        # Write the PDF to the selected file path
        with open(file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())

# Tkinter GUI setup
def generate_receipt():
    rent = {'Rent': float(rent_entry.get())}
    bills = {
        'Internet': float(internet_entry.get()),
        'Water': float(water_entry.get()),
        'Electric': float(electric_entry.get())
    }
    
    receipt_text = generate_receipt_text(rent, bills)
    receipt_display.delete(1.0, END)
    receipt_display.insert(END, receipt_text)

    # Reset input fields to empty strings after generating the receipt
    rent_entry.delete(0, END)
    internet_entry.delete(0, END)
    water_entry.delete(0, END)
    electric_entry.delete(0, END)

    # Set focus back to the top input box
    rent_entry.focus_set()

def download_pdf():
    receipt_text = receipt_display.get(1.0, END)
    save_pdf(receipt_text)

# Function to handle Enter key for moving to the next widget
def on_enter(event, next_widget):
    next_widget.focus_set()

# Function to handle Enter key on the last entry to trigger the Generate button
def on_final_enter(event):
    generate_receipt()

root = Tk()
root.title("Monthly Expense Receipt Generator")

# Rent and Bills Inputs
Label(root, text="Rent:").grid(row=0, column=0)
rent_entry = Entry(root)
rent_entry.grid(row=0, column=1)
rent_entry.bind("<Return>", lambda event: on_enter(event, internet_entry))

Label(root, text="Internet:").grid(row=1, column=0)
internet_entry = Entry(root)
internet_entry.grid(row=1, column=1)
internet_entry.bind("<Return>", lambda event: on_enter(event, water_entry))

Label(root, text="Water:").grid(row=2, column=0)
water_entry = Entry(root)
water_entry.grid(row=2, column=1)
water_entry.bind("<Return>", lambda event: on_enter(event, electric_entry))

Label(root, text="Electric:").grid(row=3, column=0)
electric_entry = Entry(root)
electric_entry.grid(row=3, column=1)
electric_entry.bind("<Return>", on_final_enter)  # Pressing Enter in the last entry triggers receipt generation

# Buttons to generate receipt and download as PDF
generate_button = Button(root, text="Generate Receipt", command=generate_receipt)
generate_button.grid(row=4, column=0, columnspan=2)

download_button = Button(root, text="Download as PDF", command=download_pdf)
download_button.grid(row=5, column=0, columnspan=2)

# Display area for the receipt
receipt_display = Text(root, width=60, height=20)
receipt_display.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
