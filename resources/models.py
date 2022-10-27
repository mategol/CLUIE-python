def get_model(settings, model_type):
    if model_type == 'framedlist':
        columns = []
        total_autos = 0
        total_manuals = 0
        for column in range(len(settings.columns)):
            if settings.columns[column][1] == 'auto':
                total_autos += 1
            else:
                total_manuals += settings.columns[column][1]
        for column in range(len(settings.columns)):
            if settings.columns[column][1] == 'auto':
                columns.append([settings.columns[column][0], int((settings.canvas_width-total_manuals)/total_autos)])
            else:
                columns.append(settings.columns[column])
        return columns
