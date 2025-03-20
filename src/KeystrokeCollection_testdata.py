from tkinter import *
import tkinter as tk
import threading
import time
from tkinter import messagebox
from pynput import keyboard
import mysql.connector
import bcrypt


class KeystrokeDynamicsRecorder:
    prev = None
    target = -1

    def __init__(self, root):

        self.root = root
        self.root.geometry("550x350+470+200")
        self.root.title("Keystroke Dynamics Collection for System Testing")

        self.label_name = tk.Label(root, text="Username :", font=("Verdana", 10))
        self.label_name.grid(row=1, column=0, sticky=W, padx=20, pady=20)

        self.entry_name = tk.Entry(root, width=40, font=("Verdana", 10))
        self.entry_name.grid(row=1, column=1, sticky=W)

        self.canvas = Canvas(root, width=240, height=20)
        self.canvas.grid(row=3, column=1, sticky=W)
        self.canvas.create_line(0, 10, 240, 10, dash=(5, 1))

        self.canvas = Canvas(root, width=160, height=20)
        self.canvas.grid(row=3, column=0, sticky=W)
        self.canvas.create_line(20, 10, 160, 10, dash=(5, 1))

        self.record_button = tk.Button(root, text="Start Recording", bg="gainsboro",
                                       font=("Verdana", 10), command=self.start_recording)
        self.record_button.grid(row=4, column=1, sticky=W, ipadx=20)

        self.label = tk.Label(root, text="Enter your passphrase :", font=("Verdana", 10))
        self.label.grid(row=6, column=0, sticky=W, padx=20)

        self.entry = tk.Entry(root, width=40, font=("Verdana", 10))
        self.entry.grid(row=6, column=1, pady=20, sticky=W)

        self.save_button = tk.Button(root, text="Save As Genuine User", font=("Verdana", 10),
                                     command=self.export_results)
        self.save_button.grid(row=8, column=1, sticky=E, ipadx=20, pady=10)

        self.save_button = tk.Button(root, text="Save As Unknown User", font=("Verdana", 10),
                                     command=self.export_results_intruder)
        self.save_button.grid(row=9, column=1, sticky=E, ipadx=20, pady=10)

        self.clear_button = tk.Button(root, text="Clear", font=("Verdana", 10),
                                      command=self.clear_entry)
        self.clear_button.grid(row=7, column=1, sticky=E, ipadx=20)

        self.running = False
        self.keystroke_dynamics = []

    def start_recording(self):
        if self.running:
            return

        if len(self.entry_name.get()) == 0:
            messagebox.showinfo("Notice", f"Please fill in username")
        else:
            self.running = True
            self.entry_name.config(state="disabled")
            self.record_button.config(text="Stop Recording", command=self.stop_recording)

        threading.Thread(target=self.record_keystrokes).start()

    def stop_recording(self):
        self.running = False
        self.record_button.config(text="Start Recording", command=self.start_recording)

    def record_keystrokes(self):
        with keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join()

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
                self.keystroke_dynamics.append(flight_timestamp * 1000)

            self.prev = timestamp

    def on_key_release(self, key):
        if hasattr(key, 'char'):
            key_name = key.char
        else:
            key_name = str(key)

        if key_name.isalpha() or key == keyboard.Key.space:
            dwell_timestamp = time.time() - self.prev
            self.keystroke_dynamics.append(dwell_timestamp * 1000)

    def export_results(self):
        passphrase = self.entry.get()
        if self.validate():
            self.target = 0
            connection = mysql.connector.connect(
                host="localhost",
                database="final_project")
            cursor = connection.cursor()

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(passphrase.encode('utf-8'), salt)

            key = []
            element = len(self.keystroke_dynamics)
            for x in range(element):
                key.append(self.keystroke_dynamics[x])

            for x in range(element, 49):
                key.append(0)

            insert_query = "INSERT INTO testset (User_ID, Target, key_1, key_2, key_3, key_4, " \
                           "key_5, key_6, key_7, key_8, key_9, key_10, " \
                           "key_11, key_12, key_13, key_14, key_15, key_16, key_17, key_18, key_19, key_20, " \
                           "key_21, key_22, key_23, key_24, key_25, key_26, key_27, key_28, key_29, key_30, " \
                           "key_31, key_32, key_33, key_34, key_35, key_36, key_37, key_38, key_39, key_40, " \
                           "key_41, key_42, key_43, key_44, key_45, key_46, key_47, key_48, key_49) VALUES " \
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                           ", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                           ", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            data_values = (self.entry_name.get(), self.target,
                           key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7], key[8], key[9],
                           key[10], key[11], key[12], key[13], key[14], key[15], key[16], key[17], key[18], key[19],
                           key[20], key[21], key[22], key[23], key[24], key[25], key[26], key[27], key[28], key[29],
                           key[30], key[31], key[32], key[33], key[34], key[35], key[36], key[37], key[38], key[39],
                           key[40], key[41], key[42], key[43], key[44], key[45], key[46], key[47], key[48])

            cursor.execute(insert_query, data_values)
            connection.commit()
            cursor.close()
            connection.close()

            self.keystroke_dynamics.clear()
            self.entry.delete(0, tk.END)
            self.prev = None

    def export_results_intruder(self):
        passphrase = self.entry.get()
        if self.validate():
            connection = mysql.connector.connect(
                host="localhost",
                database="final_project")
            cursor = connection.cursor()

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(passphrase.encode('utf-8'), salt)

            key = []
            element = len(self.keystroke_dynamics)
            for x in range(element):
                key.append(self.keystroke_dynamics[x])

            for x in range(element, 49):
                key.append(0)

            insert_query = "INSERT INTO mixset (User_ID, Target, key_1, key_2, key_3, key_4, " \
                           "key_5, key_6, key_7, key_8, key_9, key_10, " \
                           "key_11, key_12, key_13, key_14, key_15, key_16, key_17, key_18, key_19, key_20, " \
                           "key_21, key_22, key_23, key_24, key_25, key_26, key_27, key_28, key_29, key_30, " \
                           "key_31, key_32, key_33, key_34, key_35, key_36, key_37, key_38, key_39, key_40, " \
                           "key_41, key_42, key_43, key_44, key_45, key_46, key_47, key_48, key_49) VALUES " \
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                           ", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                           ", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            data_values = (self.entry_name.get(), self.target,
                           key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7], key[8], key[9],
                           key[10], key[11], key[12], key[13], key[14], key[15], key[16], key[17], key[18], key[19],
                           key[20], key[21], key[22], key[23], key[24], key[25], key[26], key[27], key[28], key[29],
                           key[30], key[31], key[32], key[33], key[34], key[35], key[36], key[37], key[38], key[39],
                           key[40], key[41], key[42], key[43], key[44], key[45], key[46], key[47], key[48])

            cursor.execute(insert_query, data_values)
            connection.commit()
            cursor.close()
            connection.close()

            self.keystroke_dynamics.clear()
            self.entry.delete(0, tk.END)
            self.prev = None

    def validate(self):
        passphrase = self.entry.get()
        if len(passphrase) < 20 or len(passphrase) > 25:
            messagebox.showinfo("Notice", f"Passphrase should be 20 to 25 characters.")
            self.clear_entry()
            return False
        else:
            for char in passphrase:
                if not char.islower() or char.isspace():
                    messagebox.showinfo("Notice", f"Passphrase should consist of lowercase letters only.")
                    self.clear_entry()
                    return False
                else:
                    return True

    def clear_entry(self):
        self.entry.delete(0, tk.END)
        self.keystroke_dynamics.clear()
        self.prev = None

    def run(self):
        self.root.mainloop()


root = tk.Tk()
app = KeystrokeDynamicsRecorder(root)
app.run()
