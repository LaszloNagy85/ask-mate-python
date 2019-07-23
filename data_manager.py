import connection
import util


def get_all_data(file_name):
    return connection.get_all_data_from_file(file_name)


SELECTED_DATA = 0


def get_selected_data(file_name, data_id):
    existing_data = connection.get_all_data_from_file(file_name)
    return [row for row in existing_data if row['id'] == data_id][SELECTED_DATA]

