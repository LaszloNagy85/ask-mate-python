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


def delete_answer(id_, id_key):
    remaining_answers = []
    all_answers = get_all_data('test_answers')
    for answer in all_answers:
        if id_ != answer[id_key]:
            remaining_answers.append(answer)

    return remaining_answers


def delete_question(id_):
    remaining_questions = []
    all_questions = get_all_data('test')
    for question in all_questions:
        if id_ != question['id']:
            remaining_questions.append(question)
        else:
            remaining_answers = delete_answer(id_, 'question_id')
    return remaining_questions, remaining_answers


def get_dict_of_specific_types(list_of_types, data):
    specific_data = []
    for row in data:
        specific_data.append({key: value for key, value in row.items() if key in list_of_types})
    return specific_data


def add_data(data, file_name, data_header):
    return connection.write_data_to_file(data, file_name, data_header)


def update_data(data, file_name, data_header):
    return connection.write_data_to_file(data, file_name, data_header, False)


def get_sorted_data(file_name, sort_by, direction):
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


def save_vote(question_id, type, data_header):
    existing_votes = connection.get_all_data_from_file('question')
    for row in existing_votes:
        if row['id'] == question_id:
            if type == 'up':
                row['vote_number'] = str(int(row['vote_number']) + 1) if row['vote_number'] else 1
            else:
                row['vote_number'] = str(int(row['vote_number']) - 1) if row['vote_number'] else -1
    connection.write_votes(existing_votes, 'question', data_header)