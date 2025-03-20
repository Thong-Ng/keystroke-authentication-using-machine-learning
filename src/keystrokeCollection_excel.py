from tkinter import *
import tkinter as tk
import threading
import time
from tkinter import messagebox
import pandas as pd
from pynput import keyboard

class KeystrokeDynamicsRecorder:

    prev = None

    def __init__(self, root):
        self.root = root
        self.root.title("Keystroke Dynamics Recorder")

        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.grid(row=0, column=1, sticky=W)

        self.label = tk.Label(root, text="Enter your passphrase:")
        self.label.grid(row=1, column=1, sticky=W)

        for x in range(10):
            self.label = tk.Label(root, text=str(x+1)+". ")
            self.label.grid(row=x+2, column=0)

        for x in range(10):
            self.entry = tk.Entry(root, width=50)
            self.entry.grid(row=x+2, column=1, sticky=W)

        self.label = tk.Label(root, text="Keystroke Dynamics:")
        self.label.grid(row=13, column=1, sticky=W)

        self.result_text = tk.Text(root, height=20, width=60)
        self.result_text.grid(row=14, column=1)

        self.save_button = tk.Button(root, text="Save", command=self.export_results)
        self.save_button.grid(row=15, column=1, sticky=W)

        self.running = False
        self.keystroke_dynamics = []

    def start_recording(self):
        if self.running:
            return

        self.running = True
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
                self.keystroke_dynamics.append(("DD_KEY : " + key_name, flight_timestamp*1000))

            self.prev = timestamp

    def on_key_release(self, key):
        if hasattr(key, 'char'):
            key_name = key.char
        else:
            key_name = str(key)
        if key_name.isalpha() or key == keyboard.Key.space:
            dwell_timestamp = time.time() - self.prev
            self.keystroke_dynamics.append(("H_KEY : " + key_name, dwell_timestamp*1000))
            self.update_results()

    def update_results(self):
        self.result_text.delete(1.0, tk.END)
        for key, timestamp in self.keystroke_dynamics:
            self.result_text.insert(tk.END, f"{key}, {timestamp:.4f}\n")

    def export_results(self):
        df = pd.DataFrame(self.keystroke_dynamics)
        df.to_excel('123keystroke.xlsx', index=False)
        messagebox.showinfo("Notice", "Data collected")

    def run(self):
        self.root.mainloop()

root = tk.Tk()
app = KeystrokeDynamicsRecorder(root)
app.run()
