from colorama import init, Fore, Back, Style
from math import floor
from pynput import keyboard
import os
import cursor

init(autoreset=True)

class engine:
    def __init__(self, model, resolution, controlling_keys):
        self.settings = {
            'margin_left': 0,
            'margin_right': 0,
            'margin_top': 0,
            'margin_bottom': 0,
            'top_header': [],
            'bottom_footer': [],
            'pointer': '',
            'column_label_margin': 0,
            'row_entry_margin': 0,
            'list_scroll_margin': 1
        }

        self.submitted = []
        self.position = [0, 0]
        self.content = []
        self.content_ids = []
        self.columns = []

        try:
            self.canvas_width = int(resolution.split('x')[0])
            self.canvas_height = int(resolution.split('x')[1])
            self.view_anchor = 1
            os.system('mode ' + str(self.canvas_width+2) + ',' + str(self.canvas_height))
        except:
            print('CLUIE: Canvas resolution fetching error. Check if you typed it in following format [WIDTH]x[HEIGHT].')

        try:
            match model:
                case 'FramedList':
                    self.model = self.get_model(model)
        except Exception as err:
            print('CLUIE: Model importing error. Make sure it\'s placed in the same folder and is properly prepared.' + str(err))
        
        try:
            match controlling_keys:
                case 'WSADE':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'w', 's', 'a', 'd', 'Key.enter'
                case 'ARROWSE':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.enter'
                case 'WSADS':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'w', 's', 'a', 'd', 'Key.space'
                case 'ARROWSS':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.space'
                case _:
                    self.key_up = controlling_keys[0]
                    self.key_down = controlling_keys[1]
                    self.key_left = controlling_keys[2]
                    self.key_right = controlling_keys[3]
                    self.key_submit = controlling_keys[4]
        except:
            print('CLUIE: Controlling keys assign error. Check documentation for more information.')

    def save(self, name):
        with open((name if name[-5:] != '.menu' else name[:-5]) + '.menu', 'w') as save_menu:
            save_menu.write(str(self.canvas_width) + '\n')
            save_menu.write(str(self.canvas_height) + '\n')
            save_menu.write(str(self.settings) + '\n')
            save_menu.write(str(self.columns) + '\n')
            save_menu.write(str(self.column_widths) + '\n')
            save_menu.write(str(self.content) + '\n')
            save_menu.write(str(self.content_ids) + '\n')

    def load(self, name):
        with open((name if name[-5:] != '.menu' else name[:-5]) + '.menu', 'r') as load_menu:
            data = load_menu.readlines()
        exec('self.canvas_width = ' + str(data[0][:-1]))
        exec('self.canvas_height = ' + str(data[1][:-1]))
        exec('self.settings = ' + str(data[2][:-1]))
        exec('self.columns = ' + str(data[3][:-1]))
        exec('self.column_widths = ' + str(data[4][:-1]))
        exec('self.content = ' + str(data[5][:-1]))
        exec('self.content_ids = ' + str(data[6][:-1]))
        self.model = self.get_model(self, self.model['model_id'])
        os.system('mode ' + str(self.canvas_width+2+int(self.settings['margin_left']+self.settings['margin_right'])) + ',' + str(self.canvas_height+self.settings['margin_top']+self.settings['margin_bottom']))

    def display(self):
        listener = keyboard.Listener(on_press=self.on_press).start()
        self.update_canvas(None)
        cursor.hide()

    def configure(self, setting, value=None):
        if type(setting) == list:
            for i in setting:
                self.configure(i[0], i[1])
        elif value != None:
            if setting in self.settings.keys():
                self.settings[setting] = value
                match setting:
                    case 'margin_left'|'margin_right'|'margin_top'|'margin_bottom':
                        os.system('mode ' + str(self.canvas_width+2+int(self.settings['margin_left']+self.settings['margin_right'])) + ',' + str(self.canvas_height+self.settings['margin_top']+self.settings['margin_bottom']))
                self.model = self.get_model(self.model['model_id'])
            else:
                print('CLUIE: There is no such setting as ' + str(setting) + '. Check documentation for available settings to configure.')
        else:
            print('CLUIE: You cannot leave empty value.')

    def add_row(self, row, id=None):
        if type(row) == str:
            row = [row]
        if len(row) > len(self.columns):
            row = row[:len(self.columns)]
        elif len(row) < len(self.columns):
            for i in range(len(self.columns)-len(row)):
                row.append('')
        self.content_ids.append(id)
        self.content.append(list(map(str, row)))

    def add_column(self, name, width='auto'):
        if type(name) == list:
            for column in name:
                self.add_column(column[0], column[1] if len(column) > 1 else 'auto')
        else:
            if len(self.columns) == 0 or (0 not in self.calculate_widths([name, width]) and 1 not in self.calculate_widths([name, width]) and 2 not in self.calculate_widths([name, width])):
                self.columns.append([name, width])
                self.model = self.get_model(self.model['model_id'])
                self.column_widths = self.calculate_widths()
            else:
                print('CLUIE: One column must be at least 3 units wide.')

    def await_submission(self):
        with keyboard.Events() as events:
            for event in events:
                if str(event.key) == self.key_submit:
                    break
        temp = self.submitted
        self.submitted = []
        return temp

    def on_press(self, key):
        key = str(key).replace('\'', '')
        pressed_key = None
        match key:
            case self.key_up: pressed_key = 'up'; self.position[1] -= 1
            case self.key_down: pressed_key = 'down'; self.position[1] += 1
            case self.key_left: pressed_key = 'left'; self.position[0] += 1
            case self.key_right: pressed_key = 'right'; self.position[0] -= 1
            case self.key_submit:
                if self.model['model_id'] == 'FramedList':
                    self.submitted = [self.content[self.position[1]], self.content_ids[self.position[1]]]
                pressed_key = 'submit'; self.position = [0, 0]; self.view_anchor = 1
        if pressed_key != None: self.update_canvas(pressed_key)

    def update_canvas(self, reason):
        content = []
        for row in range(len(self.content)):
            content.append([])
            for cell in range(len(self.content[row])):
                if len(self.content[row][cell]) > self.column_widths[cell]-self.settings['row_entry_margin']-len(self.settings['pointer']):
                    content[-1].append(self.content[row][cell][:self.column_widths[cell]-self.settings['row_entry_margin']-len(self.settings['pointer'])-1]+'…')
                else:
                    content[-1].append(self.content[row][cell])

        if self.model['model_id'] == 'FramedList':
            ready_row = ''
            os.system('cls')
            print(self.model['first_row'] + '\n' + self.model['second_row'] + '\n' + self.model['third_row'])
            if self.position[1] > len(content)-1:
                self.position[1] = len(content)-1
            elif self.position[1] < 0:
                self.position[1] = 0

            if len(content) > self.canvas_height-4:
                if self.position[1] > self.view_anchor + floor(self.canvas_height-4-self.settings['list_scroll_margin']-1):
                    self.view_anchor += 1
                elif self.position[1] < self.view_anchor + self.settings['list_scroll_margin'] and self.view_anchor > 0:
                    self.view_anchor -= 1
            else:
                self.view_anchor = 0

            for row in range(self.view_anchor, self.view_anchor+floor(self.canvas_height-4)):
                ready_row = self.settings['margin_left']*' '
                if row == self.position[1]:
                    ready_row += self.model['divider'] + self.settings['pointer'] + Back.WHITE + Fore.BLACK
                    for cell in range(len(content[row])):
                        ready_row += ' '*self.settings['row_entry_margin'] + content[row][cell] + ' '*(self.column_widths[cell]-len(content[row][cell])+1-self.settings['row_entry_margin']-(len(self.settings['pointer']) if cell == 0 else 0))
                    ready_row = ready_row[:-1] + Back.RESET + Fore.RESET + self.model['divider']
                elif row < len(content):
                    ready_row += self.model['divider']
                    for cell in range(len(content[row])):
                        ready_row += ' '*(self.settings['row_entry_margin']+(len(self.settings['pointer']) if cell == 0 else 0)) + content[row][cell] + ' '*(self.column_widths[cell]-len(content[row][cell])-self.settings['row_entry_margin']-(len(self.settings['pointer']) if cell == 0 else 0)) + self.model['divider']
                else:
                    ready_row += self.model['divider']
                    for cell in range(len(self.column_widths)):
                        ready_row += ' '*((self.column_widths[cell])) + self.model['divider']
                print(ready_row)
            last_row, footer = self.settings['margin_left']*' ' + '┗', ''
            for column in range(len(self.column_widths)):
                last_row += '━'*self.column_widths[column] + '┻'

            if len(self.settings['bottom_footer']) > 0:
                if len(self.settings['bottom_footer']) > self.settings['margin_bottom']:
                    footer = '\n' + '\n'.join(self.settings['bottom_footer'][:self.settings['margin_bottom']])
                else:
                    footer = '\n' + '\n'.join(self.settings['bottom_footer']) + (self.settings['margin_bottom']-len(self.settings['bottom_footer']))*'\n'
            else:
                footer = self.settings['margin_bottom']*'\n'

            print(last_row[:-1] + '┛' + self.settings['margin_right']*' ' + footer, end='\r')

    def calculate_widths(self, new_column=None):
        columns, raw_columns = [], []
        for i in self.columns:
            raw_columns.append(i)
        total_autos, total_manuals = 0, 0
        if new_column != None:
            raw_columns.append(new_column)
        for column in range(len(raw_columns)):
            if raw_columns[column][1] == 'auto':
                total_autos += 1
            else:
                total_manuals += raw_columns[column][1]
        for column in range(len(raw_columns)):
            if raw_columns[column][1] == 'auto':
                columns.append(int((self.canvas_width-total_manuals-len(raw_columns)+1)/total_autos))
            else:
                columns.append(raw_columns[column][1])
        return columns

    def get_model(self, model_type):
        columns = []
        column_sizes = self.calculate_widths()
        first_row, second_row, third_row = self.settings['margin_left']*' ' + '┏', self.settings['margin_left']*' ' + '┃', self.settings['margin_left']*' ' + '┣'
        for i in range(len(self.columns)):
            columns.append([self.columns[i][0], column_sizes[i]])
            first_row += '━'*columns[i][1] + '┳'
            second_row += ((' '*self.settings['column_label_margin'] + columns[i][0] + ' '*(columns[i][1]-len(columns[i][0])-self.settings['column_label_margin'])) if len(columns[i][0])+self.settings['column_label_margin'] <= columns[i][1] else (columns[i][0][:columns[i][1]-1-self.settings['column_label_margin']] + '…')) + '┃'
            third_row += '━'*columns[i][1] + '╋'
        first_row, third_row = first_row[:-1] + '┓', third_row[:-1] + '┫'
        if len(self.settings['top_header']) > 0:
            if len(self.settings['top_header']) > self.settings['margin_top']:
                header = '\n'.join(self.settings['top_header'][:self.settings['margin_top']])
            else:
                header = '\n'.join(self.settings['top_header']) + (self.settings['margin_top']-len(self.settings['top_header']))*'\n'
        else:
            header = self.settings['margin_top']*'\n'
        return {'model_id': 'FramedList', 'first_row': header + '\n' + first_row + self.settings['margin_right']*' ', 'second_row': second_row + self.settings['margin_right']*' ', 'third_row': third_row + self.settings['margin_right']*' ', 'divider': '┃', 'columns': columns}
