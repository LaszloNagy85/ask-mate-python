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


def convert_readable_dates(data):
    for row in data:
        row['submission_time'] = util.convert_epoch_to_readable(row['submission_time'])


def get_dict_of_specific_types(list_of_types, file_name):
    specific_data = []
    all_data = get_all_data(file_name)
    for row in all_data:
        specific_data.append({key: value for key, value in row.items() if key in list_of_types})
    return specific_data


def add_data(data, file_name, data_header):
    return connection.write_data_to_file(data, file_name, data_header)


def update_data(data, file_name, data_header):
    return connection.write_data_to_file(data, file_name, data_header, False)
