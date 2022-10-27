import resources.view_generator
from pynput import keyboard

def on_press(key):
    print(key)

listener = keyboard.Listener(on_press=on_press).start()
