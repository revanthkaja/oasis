#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")

        self.label_location = tk.Label(master, text="Enter Location:")
        self.label_location.grid(row=0, column=0, padx=10, pady=5)

        self.entry_location = tk.Entry(master)
        self.entry_location.grid(row=0, column=1, padx=10, pady=5)

        self.search_button = tk.Button(master, text="Search", command=self.search_weather)
        self.search_button.grid(row=0, column=2, padx=10, pady=5)

        self.label_weather_icon = tk.Label(master)
        self.label_weather_icon.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.label_temperature = tk.Label(master, font=('Helvetica', 24))
        self.label_temperature.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        self.label_conditions = tk.Label(master)
        self.label_conditions.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def search_weather(self):
        location = self.entry_location.get()
        if not location:
            messagebox.showerror("Error", "Please enter a location.")
            return

        api_key = 'YOUR_API_KEY'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        
        try:
            response = requests.get(url)
            data = response.json()
            if data['cod'] != 200:
                messagebox.showerror("Error", "Invalid location. Please try again.")
                return

            temperature = data['main']['temp']
            conditions = data['weather'][0]['description']
            icon_code = data['weather'][0]['icon']

            self.update_weather_display(temperature, conditions, icon_code)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_weather_display(self, temperature, conditions, icon_code):
        temperature_str = f"{temperature} °C"
        self.label_temperature.config(text=temperature_str)

        icon_url = f'http://openweathermap.org/img/w/{icon_code}.png'
        image = self.load_image_from_url(icon_url)
        if image:
            self.label_weather_icon.config(image=image)
            self.label_weather_icon.image = image
        
        self.label_conditions.config(text=conditions)

    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            photo_image = ImageTk.PhotoImage(image)
            return photo_image
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            return None

root = tk.Tk()
app = WeatherApp(root)
root.mainloop()


# In[ ]:




