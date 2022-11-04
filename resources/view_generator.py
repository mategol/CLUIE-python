from colorama import init, Fore, Back, Style
from os import system
from math import floor, ceil

init(autoreset=True)

def update_canvas(reason, model, position, content_raw, settings, view_anchor, controller):
    content = []
    for row in range(len(content_raw)):
        content.append([])
        for cell in range(len(content_raw[row])):
            if len(content_raw[row][cell]) > settings[cell]-controller.settings['row_entry_margin']:
                content[-1].append(content_raw[row][cell][:settings[cell]-controller.settings['row_entry_margin']-1]+'…')
            else:
                content[-1].append(content_raw[row][cell])

    if model['model_id'] == 'FramedList':
        ready_row = ''
        system('cls')
        print(model['first_row'] + '\n' + model['second_row'] + '\n' + model['third_row'])
        if position[1] > len(content)-1:
            position[1] = len(content)-1
            controller.position[1] = len(content)-1
        elif position[1] < 0:
            position[1] = 0

        for row in range(view_anchor-floor((controller.canvas_height-4)/2), view_anchor+ceil((controller.canvas_height-4)/2)):
            if row == position[1]:
                ready_row = model['divider'] + Back.WHITE + Fore.BLACK
                for cell in range(len(content[row])):
                    ready_row += ' '*controller.settings['row_entry_margin'] + content[row][cell] + ' '*(settings[cell]-len(content[row][cell])+1-controller.settings['row_entry_margin'])
                ready_row = ready_row[:-1] + Back.RESET + Fore.RESET + model['divider']
            elif row < len(content):
                ready_row = model['divider']
                for cell in range(len(content[row])):
                    ready_row += ' '*controller.settings['row_entry_margin'] + content[row][cell] + ' '*(settings[cell]-len(content[row][cell])-controller.settings['row_entry_margin']) + model['divider']
            else:
                ready_row = model['divider']
                for cell in range(len(settings)):
                    ready_row += ' '*((settings[cell])) + model['divider']
            print(ready_row)
        last_row = '┗'
        for column in range(len(settings)):
            last_row += '━'*settings[column] + '┻'
        print(last_row[:-1] + '┛', end='\r')
