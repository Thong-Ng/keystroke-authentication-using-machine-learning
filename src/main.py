import time
import keyboard

def record_keystrokes():
    keystrokes = []
    prev_time = time.time()

    #def on_key_press():


    def on_key_release(event):
        #s = event.text()
        #if s.isalpha():
        nonlocal prev_time
        current_time = time.time()
        time_diff = current_time - prev_time

        keystrokes.append((event.name, time_diff))
        prev_time = current_time

    #keyboard.on_press(on_key_press)
    keyboard.on_release(on_key_release)


    keyboard.wait('enter')

    for keystroke in keystrokes:
        print(f"\nKey: {keystroke[0]}, Time: {keystroke[1]} seconds")

record_keystrokes()
