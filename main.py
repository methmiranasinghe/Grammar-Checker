#Spell Checker
import enchant
from tkinter import Tk, filedialog, Button, Label
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import re

def check_spelling(file_path):
    with open(file_path, 'r') as file:
        text_content = file.read()

    # Use enchant to check for spelling errors
    dictionary = enchant.Dict("en_US")
    words = re.findall(r'\b\w+\b', text_content)  # Extract alphabetic words
    spelling_errors = [word for word in words if not is_correctly_spelled(word, dictionary)]

    # Display the spelling errors
    if spelling_errors:
        error_messages = "\n".join([f"Spelling Error: {word}" for word in spelling_errors])
        result_label.config(text=f"Spelling Errors:\n{error_messages}")

        # Save spelling errors to a PDF file
        save_to_pdf(spelling_errors, file_path)
    else:
        result_label.config(text="No spelling errors found.")

def is_correctly_spelled(word, dictionary):
    # Helper function to check if a word is correctly spelled
    return dictionary.check(word)

def save_to_pdf(errors, file_path):
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    pdf_file_path = f"{base_name}_spelling_errors.pdf"
    
    try:
        with open(pdf_file_path, 'w'):  # Create an empty file to check if the location is writable
            pass
    except PermissionError:
        # If the PermissionError occurs, use the current working directory
        pdf_file_path = f"{os.getcwd()}\\{base_name}_spelling_errors.pdf"

    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, "Spelling Errors in Text:")
    c.drawString(100, 730, "-" * 50)

    y_position = 710
    for error in errors:
        c.drawString(100, y_position, str(error))
        y_position -= 15

    c.save()
    result_label.config(text=f"Spelling errors saved to: {pdf_file_path}")

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )
    if file_path:
        check_spelling(file_path)

# Create the main window
root = Tk()
root.title("Text Spelling Checker")

# Add a button to browse and upload a file
browse_button = Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=20)

# Add a label to display the error messages
result_label = Label(root, text="")
result_label.pack()

# Start the GUI event loop
root.mainloop()

