def get_id(existing_data, change=1):

    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + change)
