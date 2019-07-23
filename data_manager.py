import connection
import util


def get_all_data(file_name):
    return connection.get_all_data_from_file(file_name)


def get_selected_data(file_name, data_id, data_key):
    existing_data = connection.get_all_data_from_file(file_name)
    return [row for row in existing_data if row[data_key] == data_id]


def get_all_data_of_one_type(type_, file_name):
    existing_data = connection.get_all_data_from_file(file_name)
    selected_data = []
    for row in existing_data:
        selected_data.append(row[type_])
    return selected_data


def generate_id(file_name):
    all_data = connection.get_all_data_from_file(file_name)
    return util.get_id(all_data)