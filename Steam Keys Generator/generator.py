import random
import string
import os
import tkinter as tk
from tkinter import messagebox

def generate_key():
    parts = []
    for _ in range(3):
        part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        parts.append(part)
    return '-'.join(parts)

def get_next_filename(folder):
    i = 1
    while True:
        filename = f"steam_keys-{i}.txt"
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1

def save_keys(keys, folder=None):
    if folder is None:
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Steam_Keys")
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    filepath = get_next_filename(folder)
    with open(filepath, "w") as f:
        for key in keys:
            f.write(key + "\n")
    return filepath

stop_loop = False

def generate_and_show(amount):
    keys = [generate_key() for _ in range(amount)]
    filepath = save_keys(keys)
    status_label.config(text=f"Generated {amount} keys in {filepath}")
    # messagebox.showinfo("Done", f"Generated {amount} keys!\nSaved in '{filepath}'.")

def loop_generate(amount):
    global stop_loop
    while not stop_loop:
        keys = [generate_key() for _ in range(amount)]
        filepath = save_keys(keys)
        status_label.config(text=f"Generated {amount} keys in {filepath}")
        root.update()
        if not loop_var.get():
            break

def on_generate():
    global stop_loop
    stop_loop = False
    try:
        amount = int(entry.get())
        if amount < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number.")
        return
    status_label.config(text="Generating keys...")
    if loop_var.get():
        root.after(100, lambda: loop_generate(amount))
    else:
        generate_and_show(amount)

def on_stop():
    global stop_loop
    stop_loop = True
    status_label.config(text="Loop stopped.")
    # optional: messagebox.showinfo("Done", "Loop stopped.")

# Tkinter window
root = tk.Tk()
root.title("Steam Key Generator")
root.geometry("320x210")

label = tk.Label(root, text="How many keys to generate?")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack()
entry.insert(0, "1")

loop_var = tk.BooleanVar()
loop_check = tk.Checkbutton(root, text="Loop Mode", variable=loop_var)
loop_check.pack(pady=5)

button = tk.Button(root, text="Generate", command=on_generate)
button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=on_stop)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="Ready to generate keys.")
status_label.pack(pady=10)

root.mainloop()
# This code is a simple Steam key generator with a GUI using Tkinter.
# It allows users to generate a specified number of keys, save them to a file,