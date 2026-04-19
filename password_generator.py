import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    username = entry_username.get()
    favourite = entry_fav.get()
    
    try:
        length = int(entry_length.get())
    except:
        messagebox.showerror("Error", "Enter valid length")
        return

    if length < 3:
        messagebox.showerror("Error", "Length should be at least 3")
        return

    # Ensure username + favourite are included
    base = username + favourite

    # Remaining length
    remaining_length = length - len(base)

    if remaining_length < 0:
        messagebox.showerror("Error", "Length too small for given inputs")
        return

    characters = string.ascii_letters + string.digits + string.punctuation

    random_part = ''.join(random.choice(characters) for _ in range(remaining_length))

    password = list(base + random_part)
    random.shuffle(password)

    final_password = ''.join(password)

    result_label.config(text="Generated Password: " + final_password)


# UI Window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")

# Username
tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

# Favourite
tk.Label(root, text="Favourite Thing").pack()
entry_fav = tk.Entry(root)
entry_fav.pack()

# Length
tk.Label(root, text="Password Length").pack()
entry_length = tk.Entry(root)
entry_length.pack()

# Button
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

# Result
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()