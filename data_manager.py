import connection
import database_connection
import util


def get_all_data(file_name):  # Z
    return connection.get_all_data_from_file(file_name)


def get_selected_data(file_name, data_id, data_key):  # N (2 kell: fetchone, fetchall)
    existing_data = connection.get_all_data_from_file(file_name)
    return [row for row in existing_data if row[data_key] == data_id]


def get_all_data_of_one_type(type_, file_name):  # do we need this?
    existing_data = connection.get_all_data_from_file(file_name)
    selected_data = []
    for row in existing_data:
        selected_data.append(row[type_])
    return selected_data


def generate_id(file_name):  # delete
    all_data = connection.get_all_data_from_file(file_name)
    return util.get_id(all_data)


def convert_readable_dates(data):  # delete
    for row in data:
        row['submission_time'] = util.convert_epoch_to_readable(row['submission_time'])


def delete_answer(id_, id_key):  # E
    remaining_answers = []
    all_answers = get_all_data('answer')
    for answer in all_answers:
        if id_ != answer[id_key]:
            remaining_answers.append(answer)

    connection.write_remaining_data_to_file(remaining_answers, 'answer', connection.DATA_HEADER_ANSWER)


def delete_question(id_):  # E
    remaining_questions = []
    all_questions = get_all_data('question')
    for question in all_questions:
        if id_ != question['id']:
            remaining_questions.append(question)
        else:
            delete_answer(id_, 'question_id')
    connection.write_remaining_data_to_file(remaining_questions, 'question', connection.DATA_HEADER_QUESTION)


def get_dict_of_specific_types(list_of_types, data):  # Z
    specific_data = []
    for row in data:
        specific_data.append({key: value for key, value in row.items() if key in list_of_types})
    return specific_data


def add_data(data, file_name, data_header):  # Z
    return connection.write_data_to_file(data, file_name, data_header)


def update_data(data, file_name, data_header):  # Z
    return connection.write_data_to_file(data, file_name, data_header, False)


def get_sorted_data(file_name, sort_by, direction):  # N
    data_to_sort = get_all_data(file_name)
    if sort_by == 'title':
        is_int = str
    else:
        is_int = int
    if direction == 'asc':
        is_reverse = False
    else:
        is_reverse = True
    sorted_data = sorted(data_to_sort, key=lambda x: is_int(x[sort_by]), reverse=is_reverse)
    return sorted_data


def save_vote(file_name, question_id, vote_type, data_header, answer_id):  # Z
    existing_votes = connection.get_all_data_from_file(file_name)
    voted_id = question_id if answer_id == 'None' else answer_id
    for row in existing_votes:
        if row['id'] == voted_id:
            if vote_type == 'up':
                row['vote_number'] = str(int(row['vote_number']) + 1) if row['vote_number'] else 1
            else:
                row['vote_number'] = str(int(row['vote_number']) - 1) if row['vote_number'] else -1
    connection.write_votes(existing_votes, file_name, data_header)


def save_image(upload_path, request_files):
    if 'image' in request_files:
        image = request_files['image']
        if image.filename != "":
            database_connection.upload_image(upload_path, image)
    else:
        image = ''
    return image


def delete_image(image_filenames, image_path):
    for filename in image_filenames:
        if filename:
            database_connection.remove_image(filename, image_path)


