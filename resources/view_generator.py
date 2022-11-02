from colorama import init, Fore, Back, Style
from os import system

init(autoreset=True)

def update_canvas(reason, model, position, content, settings, view_anchor, controller):
    if model['model_id'] == 'FramedList':
        ready_row = ''
        system('cls')
        print(model['first_row'] + '\n' + model['second_row'] + '\n' + model['third_row'])
        if position[1] > len(content)-1:
            position[1] = len(content)-1
            controller.position[1] = len(content)-1
        elif position[1] < 0:
            position[1] = 0

        for row in range(view_anchor-8, view_anchor+8):
            if row == position[1]:
                ready_row = model['divider'] + Back.WHITE + Fore.BLACK
                for cell in range(len(content[row])):
                    ready_row += content[row][cell] + ' '*(settings[cell]-len(content[row][cell])+1)
                ready_row = ready_row[:-1] + Back.RESET + Fore.RESET + model['divider']
            elif row < len(content):
                ready_row = model['divider']
                for cell in range(len(content[row])):
                    ready_row += content[row][cell] + ' '*(settings[cell]-len(content[row][cell])) + model['divider']
            else:
                ready_row = model['divider']
                for cell in range(len(settings)):
                    ready_row += ' '*((settings[cell])) + model['divider']
            print(ready_row)