from datetime import datetime
from tkinter import Tk, Label, Entry, Button, Text, END, Frame
from tkinter import ttk
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
    
    # Generate the receipt text
    receipt_text = generate_receipt_text(rent, bills)
    
    # Enable the display area for updates
    receipt_display.config(state="normal")
    
    # Clear any existing content and insert new receipt text
    receipt_display.delete(1.0, END)
    receipt_display.insert(END, receipt_text)
    
    # Disable the display area to make it read-only again
    receipt_display.config(state="disabled")

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

# Setting up the main window with styling options
root = Tk()
root.title("Rent Receipt Generator")
root.configure(bg="#f0f0f0")

# Custom styles for rounded, borderless purple buttons with black text
style = ttk.Style()
style.theme_use("default")
style.configure("RoundedButton.TButton",
                font=("Arial", 10),
                padding=(10, 5),  # Normal padding
                relief="flat",
                background="#800080",  # Purple background
                foreground="white",  # White text color
                borderwidth=0,
                focuscolor="")  # Remove focus border
style.map("RoundedButton.TButton",
          background=[("active", "#6a006a")],  # Darker purple on hover
          foreground=[("active", "#333333")],  # Lighter black text on hover
          padding=[("active", (12, 7))])  # Pop effect on hover

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

# Function to generate receipt text based on user-provided data
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

# Placeholder header label
header_label = Label(root, text="Rent Receipt", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="black")
header_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")

# Display area for the receipt with rounded corners and shadow effect
receipt_display = Text(root, width=60, height=20, relief="flat", bg="#f7f7f7", font=("Arial", 10), highlightbackground="#ddd", highlightthickness=1)
receipt_display.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
receipt_display.config(state="disabled")

# Create a frame to group input fields and style them
input_frame = Frame(root, bg="#f0f0f0")
input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="w")

Label(input_frame, text="Rent:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
rent_entry = Entry(input_frame, relief="flat", highlightbackground="#ddd", highlightthickness=1, font=("Arial", 10))
rent_entry.grid(row=0, column=1, padx=5, pady=5)
rent_entry.bind("<Return>", lambda event: on_enter(event, internet_entry))

Label(input_frame, text="Internet:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
internet_entry = Entry(input_frame, relief="flat", highlightbackground="#ddd", highlightthickness=1, font=("Arial", 10))
internet_entry.grid(row=1, column=1, padx=5, pady=5)
internet_entry.bind("<Return>", lambda event: on_enter(event, water_entry))

Label(input_frame, text="Water:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
water_entry = Entry(input_frame, relief="flat", highlightbackground="#ddd", highlightthickness=1, font=("Arial", 10))
water_entry.grid(row=2, column=1, padx=5, pady=5)
water_entry.bind("<Return>", lambda event: on_enter(event, electric_entry))

Label(input_frame, text="Electric:", bg="#f0f0f0", font=("Arial", 10)).grid(row=3, column=0, sticky="w")
electric_entry = Entry(input_frame, relief="flat", highlightbackground="#ddd", highlightthickness=1, font=("Arial", 10))
electric_entry.grid(row=3, column=1, padx=5, pady=5)
electric_entry.bind("<Return>", on_final_enter)

# Buttons to generate receipt and download as PDF with rounded style
button_frame = Frame(root, bg="#f0f0f0")
button_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nw")

generate_button = ttk.Button(button_frame, text="Generate Receipt", command=lambda: generate_receipt(),
                             style="RoundedButton.TButton")
generate_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

download_button = ttk.Button(button_frame, text="Download as PDF", command=lambda: download_pdf(),
                             style="RoundedButton.TButton")
download_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Function to generate the receipt, update the display area, and change the header
def generate_receipt(): 
    rent = {'Rent': float(rent_entry.get())}
    bills = {
        'Internet': float(internet_entry.get()),
        'Water': float(water_entry.get()),
        'Electric': float(electric_entry.get())
    }
    
    # Generate the receipt text
    receipt_text = generate_receipt_text(rent, bills)
    
    # Enable the display area for updates
    receipt_display.config(state="normal")
    
    # Clear any existing content and insert new receipt text
    receipt_display.delete(1.0, END)
    receipt_display.insert(END, receipt_text)
    
    # Disable the display area to make it read-only again
    receipt_display.config(state="disabled")

    # Update header to show the current month and year
    header_label.config(text=f"{datetime.now().strftime('%B %Y')} Rent Receipt")

    # Reset input fields to empty strings after generating the receipt
    rent_entry.delete(0, END)
    internet_entry.delete(0, END)
    water_entry.delete(0, END)
    electric_entry.delete(0, END)

    # Set focus back to the top input box
    rent_entry.focus_set()

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
        
        # Set font for the PDF
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

# Function for the download button to capture and save the receipt
def download_pdf():
    receipt_text = receipt_display.get(1.0, END).strip()  # Get the receipt content
    if receipt_text:
        save_pdf(receipt_text)  # Save as PDF if there is content
    else:
        print("No receipt text to save")

# Run the main event loop
root.mainloop()