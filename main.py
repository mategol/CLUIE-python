import resources.view_generator as vgen
from pynput import keyboard

class CLUIEngine:
    def __init__(self, model, resolution, controlling_keys):
        self.position = [0, 0]
        self.content = []
        try:
            self.canvas_width = int(resolution.split('x')[0])
            self.canvas_height = int(resolution.split('x')[1])
        except:
            print('CLUIE: Canvas resolution fetching error. Check if you typed it in following format [WIDTH]x[HEIGHT].')

        try:
            with open('model.cluie', 'r', encoding='utf-8') as load_model:
                self.view_model = self.fetch_model(load_model.readlines())
        except:
            print('CLUIE: Model importing error. Make sure it\'s placed in the same folder and is properly prepared.')
        
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

        listener = keyboard.Listener(on_press=self.on_press).start()
    
    def fetch_model(self, model):
        print('asd')

    def on_press(self, key):
        key = str(key).replace('\'', '')
        pressed_key = None
        if key == self.key_up: pressed_key = 'up'; self.position[1] += 1
        elif key == self.key_down: pressed_key = 'down'; self.position[1] -= 1
        elif key == self.key_left: pressed_key = 'left'; self.position[0] -= 1
        elif key == self.key_right: pressed_key = 'right'; self.position[0] += 1
        elif key == self.key_submit: pressed_key = 'submit'; self.position = [0, 0]
        if pressed_key != None: vgen.update_canvas(pressed_key, self.view_model, self.position, self.content)
