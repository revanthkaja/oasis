#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import socket
import json

class ChatApplication:
    def __init__(self, master):
        self.master = master
        master.title("Chat Application")

        self.message_history = scrolledtext.ScrolledText(master, state='disabled')
        self.message_history.pack(fill=tk.BOTH, expand=True)

        self.entry_message = tk.Entry(master)
        self.entry_message.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        # Create a socket
        self.server_ip = '127.0.0.1'
        self.server_port = 55555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            print(f"Error: {e}")

        # Start a separate thread for receiving messages
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.entry_message.get()
        if message:
            data = {'type': 'message', 'content': message}
            self.client_socket.sendall(json.dumps(data).encode('utf-8'))
            self.entry_message.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                self.display_message(message['content'])
            except Exception as e:
                print(f"Error: {e}")
                break

    def display_message(self, message):
        self.message_history.config(state='normal')
        self.message_history.insert(tk.END, message + '\n')
        self.message_history.config(state='disabled')
        self.message_history.see(tk.END)


root = tk.Tk()
app = ChatApplication(root)
root.mainloop()


# In[ ]:




