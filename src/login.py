import threading
import time
from pynput import keyboard
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import bcrypt
import Randomforest_demo
import Isolation_demo


class LoginInterface:
    prev = None

    def __init__(self, root):
        self.root = root
        self.root.geometry("550x410+470+220")
        self.root.title("Sign In")

        self.label_title = tk.Label(root, text="SIGN IN", font=("Verdana", 20))
        self.label_title.grid(row=0, column=0, pady=10, padx=20, sticky=E)

        self.image = Image.open("../asset/icon18.png")
        self.image = self.image.resize((160, 160))
        self.img = ImageTk.PhotoImage(self.image)
        self.label_png = Label(root, image=self.img)
        self.label_png.grid(row=1, column=1)

        self.label = tk.Label(root, text="Username :", font=("Verdana", 10))
        self.label.grid(row=2, column=0, padx=40, pady=10, sticky=E)
        self.entry_name = tk.Entry(root, width=30, font=("Verdana", 10))
        self.entry_name.grid(row=2, column=1)
        self.entry_name.focus_set()

        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(root, text="Start keystroke recording", font=("Verdana", 10),
                                       variable=self.checkbox_var, command=self.start_recording)
        self.checkbox.grid(row=9, column=1, sticky=W)

        self.label_p = tk.Label(root, text="Passphrase :", font=("Verdana", 10))
        self.label_p.grid(row=4, column=0, padx=40, pady=10, sticky=E)
        self.entry_pwd = tk.Entry(root, width=30, font=("Verdana", 10), show="*")
        self.entry_pwd.grid(row=4, column=1)
        self.button_clear = tk.Button(root, text="Clear", font=("Verdana", 10), command=self.clear_entry)
        self.button_clear.grid(row=4, column=2, ipadx=20, padx=20, pady=10, sticky=E)
        """
        self.label_n = tk.Label(root, text="Notice: Click button 'clear' if \npassphrase is wrongly typed.", font=("Verdana", 10))
        self.label_n.grid(row=5, column=1, sticky=W)
        """
        self.button = tk.Button(root, text="Login", font=("Verdana", 10), command=self.new_key)
        self.button.grid(row=8, column=1, ipadx=20, pady=10)

        #self.root.bind('<Return>', self.handle_enter)
        self.running = False
        self.keystroke_dynamics = []
        self.key = []  # new data point

    """
    def handle_enter(self, event):
        self.new_key()
    """
    def start_recording(self):
        if self.running:
            return

        self.running = True
        #self.entry_name.config(state="disabled")
        #self.checkbox.config(state="disabled")
        threading.Thread(target=self.record_keystrokes).start()

    def on_key_press(self, key):
        if not self.running:
            return False

        if hasattr(key, 'char'):
            key_name = key.char
        else:
            key_name = str(key)

        if key_name.isalpha() or key == keyboard.Key.space:

            timestamp = time.time()
            if self.prev is not None:
                flight_timestamp = timestamp - self.prev
                flight_timestamp = flight_timestamp * 1000
                self.keystroke_dynamics.append(f"{flight_timestamp:.4f}")

            self.prev = timestamp

    def on_key_release(self, key):
        if hasattr(key, 'char'):
            key_name = key.char
        else:
            key_name = str(key)

        if key_name.isalpha() or key == keyboard.Key.space:
            dwell_timestamp = time.time() - self.prev
            dwell_timestamp = dwell_timestamp * 1000
            self.keystroke_dynamics.append(f"{dwell_timestamp:.4f}")

    def record_keystrokes(self):
        with keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join()

    def new_key(self):
        element = len(self.keystroke_dynamics)
        for x in range(element):
            self.key.append(self.keystroke_dynamics[x])
        for x in range(element, 49):
            self.key.append(0)
        print(self.key)
        self.authenticate_user()

    def authenticate_user(self):
        db_connection = mysql.connector.connect(
            host="localhost",
            database="final_project"
        )
        cursor = db_connection.cursor()

        if len(self.entry_name.get()) == 0:
            messagebox.showinfo("Notice", f"Please fill in both username and passphrase.")
        else:
            if_result = Isolation_demo.isolation_demo(self.key)
            if if_result == 1:
                rf_result = Randomforest_demo.random_forest_demo(self.key)
                if rf_result == 1:
                    username = self.entry_name.get()
                    cursor.execute("SELECT User_Pwd, salt FROM keystroke WHERE User_ID = %s", (username,))
                    result = cursor.fetchone()
                    if result:
                        hashed_password, salt = result
                        salt = salt.encode('utf-8')
                        stored_hashed_password = hashed_password.encode('utf-8')
                        passphrase = self.entry_pwd.get()
                        input_hashed_password = bcrypt.hashpw(passphrase.encode('utf-8'), salt)
                        if input_hashed_password == stored_hashed_password:
                            messagebox.showinfo("Notice", f"{username} successfully login.")
                        else:
                            messagebox.showinfo("Warning", f"Invalid Username or passphrase.")
                    else:
                        messagebox.showinfo("Warning", f"Invalid Username or passphrase.")
                elif rf_result == 0:
                    messagebox.showinfo("Warning_E01", f"Staff is not allowed!")
            elif if_result == -1:
                messagebox.showinfo("Warning_E02", f"Only authorized user is allowed!")
        self.keystroke_dynamics.clear()
        self.key.clear()

    def clear_entry(self):
        self.entry_pwd.delete(0, tk.END)
        self.keystroke_dynamics.clear()
        self.key.clear()
        self.prev = None

    def run(self):
        self.root.mainloop()


root = tk.Tk()
app = LoginInterface(root)
app.run()
