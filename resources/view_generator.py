from colorama import init, Fore, Back, Style
from os import system
from math import floor, ceil

init(autoreset=True)

def update_canvas(reason, controller):
    
    content = []
    for row in range(len(controller.content)):
        content.append([])
        for cell in range(len(controller.content[row])):
            if len(controller.content[row][cell]) > controller.column_widths[cell]-controller.settings['row_entry_margin']:
                content[-1].append(controller.content[row][cell][:controller.column_widths[cell]-controller.settings['row_entry_margin']-1]+'…')
            else:
                content[-1].append(controller.content[row][cell])

    if controller.model['model_id'] == 'FramedList':
        ready_row = ''
        system('cls')
        print(controller.model['first_row'] + '\n' + controller.model['second_row'] + '\n' + controller.model['third_row'])
        if controller.position[1] > len(content)-1:
            controller.position[1] = len(content)-1
        elif controller.position[1] < 0:
            controller.position[1] = 0

        if len(content) > controller.canvas_height-4:
            if controller.position[1] > controller.view_anchor + floor((controller.canvas_height-4)/3):
                controller.view_anchor += 1
            elif controller.position[1] < controller.view_anchor - (floor((controller.canvas_height-4)/3)) and controller.position[1] > 1:
                controller.view_anchor -= 1

        for row in range(controller.view_anchor-floor((controller.canvas_height-4)/2), controller.view_anchor+ceil((controller.canvas_height-4)/2)):
            if row == controller.position[1]:
                ready_row = controller.model['divider'] + Back.WHITE + Fore.BLACK
                for cell in range(len(content[row])):
                    ready_row += ' '*controller.settings['row_entry_margin'] + content[row][cell] + ' '*(controller.column_widths[cell]-len(content[row][cell])+1-controller.settings['row_entry_margin'])
                ready_row = ready_row[:-1] + Back.RESET + Fore.RESET + controller.model['divider']
            elif row < len(content):
                ready_row = controller.model['divider']
                for cell in range(len(content[row])):
                    ready_row += ' '*controller.settings['row_entry_margin'] + content[row][cell] + ' '*(controller.column_widths[cell]-len(content[row][cell])-controller.settings['row_entry_margin']) + controller.model['divider']
            else:
                ready_row = controller.model['divider']
                for cell in range(len(controller.column_widths)):
                    ready_row += ' '*((controller.column_widths[cell])) + controller.model['divider']
            print(ready_row)
        last_row = '┗'
        for column in range(len(controller.column_widths)):
            last_row += '━'*controller.column_widths[column] + '┻'
        print(last_row[:-1] + '┛', end='\r')
