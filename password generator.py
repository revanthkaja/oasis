#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install pyperclip


# In[6]:


import tkinter as tk
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Random Password Generator")

        self.label_length = tk.Label(master, text="Password Length:")
        self.label_length.grid(row=0, column=0, padx=10, pady=5)

        self.entry_length = tk.Entry(master)
        self.entry_length.grid(row=0, column=1, padx=10, pady=5)

        self.uppercase_var = tk.IntVar()
        self.lowercase_var = tk.IntVar()
        self.digits_var = tk.IntVar()
        self.symbols_var = tk.IntVar()

        self.uppercase_check = tk.Checkbutton(master, text="Uppercase", variable=self.uppercase_var)
        self.uppercase_check.grid(row=1, column=0, padx=10, pady=5)

        self.lowercase_check = tk.Checkbutton(master, text="Lowercase", variable=self.lowercase_var)
        self.lowercase_check.grid(row=1, column=1, padx=10, pady=5)

        self.digits_check = tk.Checkbutton(master, text="Digits", variable=self.digits_var)
        self.digits_check.grid(row=2, column=0, padx=10, pady=5)

        self.symbols_check = tk.Checkbutton(master, text="Symbols", variable=self.symbols_var)
        self.symbols_check.grid(row=2, column=1, padx=10, pady=5)

        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=3, columnspan=2, padx=10, pady=10)

        self.password_label = tk.Label(master, text="")
        self.password_label.grid(row=4, columnspan=2, padx=10, pady=5)

        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=5, columnspan=2, padx=10, pady=5)

    def generate_password(self):
        length = int(self.entry_length.get())
        include_uppercase = self.uppercase_var.get()
        include_lowercase = self.lowercase_var.get()
        include_digits = self.digits_var.get()
        include_symbols = self.symbols_var.get()

        if not (include_uppercase or include_lowercase or include_digits or include_symbols):
            tk.messagebox.showerror("Error", "Select at least one character type.")
            return

        characters = ''
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_digits:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_label.config(text=password)

    def copy_to_clipboard(self):
        password = self.password_label.cget("text")
        pyperclip.copy(password)
        tk.messagebox.showinfo("Info", "Password copied to clipboard.")

root = tk.Tk()
app = PasswordGeneratorApp(root)
root.mainloop()


# In[ ]:




