#!/usr/bin/env python
# coding: utf-8

# In[12]:


import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Connect to SQLite database
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             weight REAL NOT NULL,
             height REAL NOT NULL,
             bmi REAL NOT NULL,
             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()


class BMIApp:
    def __init__(self, master):
        self.master = master
        master.title("BMI Calculator")

        self.label_weight = tk.Label(master, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0)

        self.entry_weight = tk.Entry(master)
        self.entry_weight.grid(row=0, column=1)

        self.label_height = tk.Label(master, text="Height (m):")
        self.label_height.grid(row=1, column=0)

        self.entry_height = tk.Entry(master)
        self.entry_height.grid(row=1, column=1)

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, columnspan=2)

        self.plot_button = tk.Button(master, text="Plot BMI History", command=self.plot_bmi_history)
        self.plot_button.grid(row=3, columnspan=2)

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())
            bmi = weight / (height * height)
            messagebox.showinfo("BMI Result", f"Your BMI: {bmi:.2f}")
            self.save_bmi_to_database(weight, height, bmi)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height.")

    def save_bmi_to_database(self, weight, height, bmi):
        c.execute("INSERT INTO users (name, weight, height, bmi) VALUES (?, ?, ?, ?)",
                  ('User', weight, height, bmi))
        conn.commit()

    def plot_bmi_history(self):
        c.execute("SELECT * FROM users ORDER BY timestamp")
        data = c.fetchall()
        if not data:
            messagebox.showinfo("Info", "No data to plot.")
            return

        timestamps = [row[5] for row in data]
        bmis = [row[4] for row in data]

        fig, ax = plt.subplots()
        ax.plot(timestamps, bmis)
        ax.set(xlabel='Timestamp', ylabel='BMI',
               title='BMI History')
        ax.grid()

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display plot in GUI
        fig_canvas = FigureCanvasTkAgg(fig, master=self.master)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().grid(row=4, columnspan=2, padx=10, pady=10)


root = tk.Tk()
app = BMIApp(root)
root.mainloop()

# Close database connection
conn.close()


# In[ ]:




