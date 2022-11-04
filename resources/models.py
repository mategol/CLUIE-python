def calculate_widths(settings, new_column=None):
    columns, raw_columns = [], []
    for i in settings.columns:
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
            columns.append(int((settings.canvas_width-total_manuals-len(raw_columns)+1)/total_autos))
        else:
            columns.append(raw_columns[column][1])
    return columns

def get_model(settings, model_type):
    columns = []
    column_sizes = calculate_widths(settings)
    first_row, second_row, third_row = '┏', '┃', '┣'
    for i in range(len(settings.columns)):
        columns.append([settings.columns[i][0], column_sizes[i]])
        first_row += '━'*columns[i][1] + '┳'
        second_row += ((' '*settings.settings['column_label_margin'] + columns[i][0] + ' '*(columns[i][1]-len(columns[i][0])-settings.settings['column_label_margin'])) if len(columns[i][0])+settings.settings['column_label_margin'] <= columns[i][1] else (columns[i][0][:columns[i][1]-1-settings.settings['column_label_margin']] + '…')) + '┃'
        third_row += '━'*columns[i][1] + '╋'
    first_row, third_row = first_row[:-1] + '┓', third_row[:-1] + '┫'

    return {'model_id': 'FramedList', 'first_row': first_row, 'second_row': second_row, 'third_row': third_row, 'divider': '┃', 'columns': columns}
