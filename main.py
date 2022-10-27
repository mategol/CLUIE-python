import resources.view_generator
from pynput import keyboard

class CLUIEngine:
    def __init__(self, resolution, controlling_keys):
        try:
            self.canvas_width = int(resolution.split('x')[0])
            self.canvas_height = int(resolution.split('x')[1])
        except:
            print('CLUIE: Canvas resolution fetching error. Check if you typed it in following format [WIDTH]x[HEIGHT].')
        
        try:
            if controlling_keys == 'WSADE':
                self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'w', 's', 'a', 'd', 'Key.enter'
            elif controlling_keys == 'ARROWSE':
                self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.enter'
            elif controlling_keys == 'WSADS':
                self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'w', 's', 'a', 'd', 'Key.space'
            elif controlling_keys == 'ARROWSS':
                self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.space'
            else:
                self.key_up = controlling_keys[0]
                self.key_down = controlling_keys[1]
                self.key_left = controlling_keys[2]
                self.key_right = controlling_keys[3]
                self.key_submit = controlling_keys[4]
        except:
            print('CLUIE: Controlling keys assign error. Check documentation for more information.')

        listener = keyboard.Listener(on_press=CLUIEngine.on_press).start()
    
    def on_press(key):
        print(key)
