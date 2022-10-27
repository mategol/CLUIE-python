import resources.view_generator as vgen
import resources.models as models
from pynput import keyboard

class CLUIEngine:
    def __init__(self, model, resolution, controlling_keys):
        self.position = [0, 0]
        self.canvas = {}
        self.ishidden = True

        try:
            self.canvas['width'] = int(resolution.split('x')[0])
            self.canvas['height'] = int(resolution.split('x')[1])
        except:
            print('CLUIE: Canvas resolution fetching error. Check if you typed it in following format [WIDTH]x[HEIGHT].')

        try:
            if type(model) == str:
                with open('model.cluie', 'r', encoding='utf-8') as load_model:
                    self.view_model = self.fetch_model(load_model.readlines())
            else:
                match model[0]:
                    case 'FramedList':
                        self.model = models.get_model(model[0], self.canvas_width, self.canvas_height, model[1])
        except:
            print('CLUIE: Model importing error. Make sure it\'s placed in the same folder and is properly prepared.')
        
        try:
            match controlling_keys:
                case 'WSADE':
                    self.canvas['controllers']['']
                    self.canvas['controllers']['up'], self.canvas['controllers']['down'], self.canvas['controllers']['left'], self.canvas['controllers']['right'], self.canvas['controllers']['submit'] = 'w', 's', 'a', 'd', 'Key.enter'
                case 'ARROWSE':
                    self.canvas['controllers']['up'], self.canvas['controllers']['down'], self.canvas['controllers']['left'], self.canvas['controllers']['right'], self.canvas['controllers']['submit'] = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.enter'
                case 'WSADS':
                    self.canvas['controllers']['up'], self.canvas['controllers']['down'], self.canvas['controllers']['left'], self.canvas['controllers']['right'], self.canvas['controllers']['submit'] = 'w', 's', 'a', 'd', 'Key.space'
                case 'ARROWSS':
                    self.canvas['controllers']['up'], self.canvas['controllers']['down'], self.canvas['controllers']['left'], self.canvas['controllers']['right'], self.canvas['controllers']['submit'] = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.space'
                case _:
                    self.canvas['controllers']['up'] = controlling_keys[0]
                    self.canvas['controllers']['down'] = controlling_keys[1]
                    self.canvas['controllers']['left'] = controlling_keys[2]
                    self.canvas['controllers']['right'] = controlling_keys[3]
                    self.canvas['controllers']['submit'] = controlling_keys[4]
        except:
            print('CLUIE: Controlling keys assign error. Check documentation for more information.')

        listener = keyboard.Listener(on_press=self.on_press).start()
    
    def display(self):
        self.ishidden = False

    def on_press(self, key):
        key = str(key).replace('\'', '')
        pressed_key = None
        match key:
            case self.canvas['controllers']['up']: pressed_key = 'up'; self.position[1] += 1
            case self.canvas['controllers']['down']: pressed_key = 'down'; self.position[1] -= 1
            case self.canvas['controllers']['left']: pressed_key = 'left'; self.position[0] -= 1
            case self.canvas['controllers']['right']: pressed_key = 'right'; self.position[0] += 1
            case self.canvas['controllers']['submit']: pressed_key = 'submit'; self.position = [0, 0]
        if pressed_key != None and not self.ishidden: vgen.update_canvas(pressed_key, self.view_model, self.position, self.content)
