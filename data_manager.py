import connection


def get_all_data(file_name):
    return connection.get_all_data_from_file(file_name)


def get_selected_data(file_name, data_id, data_key):
    existing_data = connection.get_all_data_from_file(file_name)
    return [row for row in existing_data if row[data_key] == data_id]
