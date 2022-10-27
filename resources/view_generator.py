from colorama import init, Fore, Back, Style
from os import system

init(autoreset=True)

def update_canvas(reason, model, position, content, settings, controller):
    if model['model_id'] == 'FramedList':
        ready_row = ''
        system('cls')
        print(model['first_row'] + '\n' + model['second_row'] + '\n' + model['third_row'])
        if position[1] > len(content)-1:
            position[1] = len(content)-1
            controller.position[1] = len(content)-1
        elif position[1] < 0:
            position[1] = 0

        for row in range(len(content)):
            if position[1] == row:
                ready_row = model['divider'] + Back.WHITE + Fore.BLACK
            for cell in range(len(content[row])):
                ready_row += model['divider'] if position[1] != row else (' ' if cell != 0 else '')
                ready_row += content[row][cell] + ' '*(settings[cell]-len(content[row][cell]))
            print(ready_row + Back.RESET + Fore.RESET + model['divider'])
            ready_row = ''
