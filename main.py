import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from datetime import datetime
import os, platform, subprocess, logging, win32print, win32api

# Set up logging
log_filename = "label_print_log.txt"
logging.basicConfig(filename=log_filename, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
LINE_SPACING = 40
BARCODE_SPACING = 90
LEFT_MARGIN = 50
PADDING = 40
PDF_FOLDER = "output_pdfs"
FONT_FAMILY = "Times-Roman"  # Built-in ReportLab font
FIELD_LABELS = ["Part Number", "Quantity", "Division", "TAB No"]

# Ensure output folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)

def validate_inputs():
    inputs = [entry.get().strip() for entry in entries]
    if any(not val for val in inputs):
        messagebox.showerror("Error", "Please fill in all fields.")
        logging.error("Validation failed: One or more fields were empty.")
        return None
    return inputs

def create_pdf(filename, part_number, quantity, division, id_number):
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        current_y = height - 100

        c.setFont(FONT_FAMILY, 48)
        c.drawString(LEFT_MARGIN, current_y, part_number)
        current_y -= LINE_SPACING

        pn_barcode = code128.Code128(part_number, barHeight=40, barWidth=1)
        pn_barcode.drawOn(c, LEFT_MARGIN, current_y - 40)
        current_y -= BARCODE_SPACING

        c.setFont(FONT_FAMILY, 40)
        c.drawString(LEFT_MARGIN, current_y, f"Quantity: {quantity}")
        current_y -= LINE_SPACING

        qty_barcode = code128.Code128(quantity, barHeight=40, barWidth=1)
        qty_barcode.drawOn(c, LEFT_MARGIN, current_y - 40)
        current_y -= BARCODE_SPACING

        c.drawString(LEFT_MARGIN, current_y, f"Division: {division}")
        current_y -= LINE_SPACING

        date_str = datetime.now().strftime("%Y-%m-%d")
        c.setFont(FONT_FAMILY, 24)
        c.drawString(PADDING, current_y, f"Date: {date_str}")
        c.drawRightString(width - PADDING, current_y, id_number)
        c.save()
        logging.info(f"PDF created successfully: {filename}")
    except Exception as e:
        logging.error(f"Failed to create PDF: {e}")
        messagebox.showerror("PDF Creation Error", f"An error occurred: {e}")

def print_pdf(filename):
    try:
        if platform.system() == "Windows":
            # Use the default system PDF viewer to print silently
            win32api.ShellExecute(
                0,
                "print",
                filename,
                None,
                ".",
                0
            )
            logging.info(f"PDF sent to printer via ShellExecute: {filename}")
            messagebox.showinfo("Success", "Label sent to printer.")
        else:
            # For Unix-like systems
            subprocess.run(["lp", filename])
            logging.info("PDF sent to default printer (Unix-like system).")
            messagebox.showinfo("Success", "Label sent to printer.")
    except Exception as e:
        logging.error(f"Failed to print PDF: {e}")
        messagebox.showerror("Print Error", f"An error occurred: {e}")

def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)

def generate_pdf_and_print():
    inputs = validate_inputs()
    if not inputs:
        return
    part_number, quantity, division, id_number = inputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(PDF_FOLDER, f"label_{part_number}-{timestamp}.pdf")
    create_pdf(filename, part_number, quantity, division, id_number)
    print_pdf(filename)
    clear_fields()

# GUI setup
root = tk.Tk()
root.title("Label Print")
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - WINDOW_HEIGHT / 2)
position_left = int(screen_width / 2 - WINDOW_WIDTH / 2)
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_left}+{position_top}')

custom_font = tkfont.Font(family="Arial", size=12)
root.config(bg="#f4f4f9")

frame = tk.Frame(root, bg="#f4f4f9")
frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

entries = []
for i, label in enumerate(FIELD_LABELS):
    tk.Label(frame, text=label + ":", font=custom_font, bg="#f4f4f9").grid(row=i, column=0, sticky="w", padx=10, pady=5)
    entry = tk.Entry(frame, font=custom_font, width=35)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

generate_button = tk.Button(
    frame, text="Generate & Print", command=generate_pdf_and_print,
    font=custom_font, bg="#4CAF50", fg="white", relief="flat", width=20
)
generate_button.grid(row=len(FIELD_LABELS), columnspan=2, pady=20)

if __name__ == "__main__":
    logging.info("Application started.")
    root.mainloop()
  
