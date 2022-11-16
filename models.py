def calculate_widths(controller, new_column=None):
    columns, raw_columns = [], []
    for i in controller.columns:
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
            columns.append(int((controller.canvas_width-total_manuals-len(raw_columns)+1)/total_autos))
        else:
            columns.append(raw_columns[column][1])
    return columns

def get_model(controller, model_type):
    columns = []
    column_sizes = calculate_widths(controller)
    first_row, second_row, third_row = controller.settings['margin_left']*' ' + '┏', controller.settings['margin_left']*' ' + '┃', controller.settings['margin_left']*' ' + '┣'
    for i in range(len(controller.columns)):
        columns.append([controller.columns[i][0], column_sizes[i]])
        first_row += '━'*columns[i][1] + '┳'
        second_row += ((' '*controller.settings['column_label_margin'] + columns[i][0] + ' '*(columns[i][1]-len(columns[i][0])-controller.settings['column_label_margin'])) if len(columns[i][0])+controller.settings['column_label_margin'] <= columns[i][1] else (columns[i][0][:columns[i][1]-1-controller.settings['column_label_margin']] + '…')) + '┃'
        third_row += '━'*columns[i][1] + '╋'
    first_row, third_row = first_row[:-1] + '┓', third_row[:-1] + '┫'
    if len(controller.settings['top_header']) > 0:
        if len(controller.settings['top_header']) > controller.settings['margin_top']:
            header = '\n'.join(controller.settings['top_header'][:controller.settings['margin_top']])
        else:
            header = '\n'.join(controller.settings['top_header']) + (controller.settings['margin_top']-len(controller.settings['top_header']))*'\n'
    else:
        header = controller.settings['margin_top']*'\n'
    return {'model_id': 'FramedList', 'first_row': header + '\n' + first_row + controller.settings['margin_right']*' ', 'second_row': second_row + controller.settings['margin_right']*' ', 'third_row': third_row + controller.settings['margin_right']*' ', 'divider': '┃', 'columns': columns}
