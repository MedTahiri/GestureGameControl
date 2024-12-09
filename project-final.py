import tkinter as tk
from PIL import ImageTk, Image
import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key


def button1_click():
    pass

def button2_click():
    pass


def button3_click():
    print("Button 3 clicked")


def button4_click():
    print("Button 4 clicked")


# Create main window
root = tk.Tk()
root.title("INSEA INNOVATION EDGE")

# Set the size of the root window
root.geometry("600x500")  # Set the width and height of the window

# Load and display image
image_path = "iie.png"  # Change this to the path of your image
image = Image.open(image_path)
image = image.resize((200, 200))  # Resize image if needed
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Add text below the image
text_label = tk.Label(root, text="festival des sciences de rabat", font=("Helvetica", 12))
text_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create buttons with titles
title1_label = tk.Label(root, text="Code 1", font=("Helvetica", 12))
title1_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))

button1 = tk.Button(root, text="Run Code", width=15, command=button1_click)  # Set the width of the button
button1.grid(row=3, column=0, padx=10, pady=10)

button2 = tk.Button(root, text="Stop", width=15, command=button2_click)  # Set the width of the button
button2.grid(row=3, column=1, padx=10, pady=10)

title2_label = tk.Label(root, text="Code 2", font=("Helvetica", 12))
title2_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

button3 = tk.Button(root, text="Run Code", width=15, command=button3_click)  # Set the width of the button
button3.grid(row=5, column=0, padx=10, pady=10)

button4 = tk.Button(root, text="Stop", width=15, command=button4_click)  # Set the width of the button
button4.grid(row=5, column=1, padx=10, pady=10)

# Center all widgets
for child in root.winfo_children():
    child.grid_configure(padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
