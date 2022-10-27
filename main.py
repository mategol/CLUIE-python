import resources.view_generator
from pynput import keyboard

class CLUIEngine:
    def __init__(self, resolution, controlling_keys):
        try:
            self.canvas_width = int(resolution.split('x')[0])
            self.canvas_height = int(resolution.split('x')[1])
        except:
            print('CLUIE: Canvas resolution fetching error. Check if you typed it in following format [WIDTH]x[HEIGHT]')

        listener = keyboard.Listener(on_press=CLUIEngine.on_press).start()
    
    def on_press(key):
        print(key)
