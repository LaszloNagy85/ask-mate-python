import connection
import database_connection
import util
from psycopg2 import sql


# def get_all_data(file_name):  # Z
#     return connection.get_all_data_from_file(file_name)


@database_connection.connection_handler
def get_all_data(cursor, table):
    query_for_func = sql.SQL('SELECT * FROM {}').format(
                     sql.Identifier(table))
    cursor.execute(query_for_func)
    all_data = cursor.fetchall()

    return all_data


# if the col_value is a string, use "'col_value'"
@database_connection.connection_handler
def get_columns_by_attribute(cursor, col_list, table, col_name, col_value):
    query_for_func = sql.SQL('SELECT {} FROM {} WHERE {} = {}').format(
        sql.SQL(', ').join(map(sql.Identifier, col_list)),
        sql.Identifier(table),
        sql.Identifier(col_name),
        sql.SQL(col_value))
    cursor.execute(query_for_func)

    if col_name == 'id':
        data = cursor.fetchone()
    else:
        data = cursor.fetchall()

    return data


def get_all_data_of_one_type(type_, file_name):  # do we need this?
    existing_data = connection.get_all_data_from_file(file_name)
    selected_data = []
    for row in existing_data:
        selected_data.append(row[type_])
    return selected_data


# def generate_id(file_name):  # delete
#     all_data = connection.get_all_data_from_file(file_name)
#     return util.get_id(all_data)


# def convert_readable_dates(data):  # delete
#     for row in data:
#         row['submission_time'] = util.convert_epoch_to_readable(row['submission_time'])


# def delete_answer(id_, id_key):  # E
#     remaining_answers = []
#     all_answers = get_all_data('answer')
#     for answer in all_answers:
#         if id_ != answer[id_key]:
#             remaining_answers.append(answer)
#
#     connection.write_remaining_data_to_file(remaining_answers, 'answer', connection.DATA_HEADER_ANSWER)


@database_connection.connection_handler
def delete_answer_db(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer)s;
                    """,
                   {'answer': answer_id})


# def delete_question(id_):  # E
#     remaining_questions = []
#     all_questions = get_all_data('question')
#     for question in all_questions:
#         if id_ != question['id']:
#             remaining_questions.append(question)
#         else:
#             delete_answer(id_, 'question_id')
#     connection.write_remaining_data_to_file(remaining_questions, 'question', connection.DATA_HEADER_QUESTION)


# def get_dict_of_specific_types(list_of_types, data):  # Z
#     specific_data = []
#     for row in data:
#         specific_data.append({key: value for key, value in row.items() if key in list_of_types})
#     return specific_data


@database_connection.connection_handler
def get_data_by_attributes(cursor, list_of_types, table):
    query_for_func = sql.SQL('SELECT {} FROM {}').format(
                     sql.SQL(', ').join(map(sql.Identifier, list_of_types)),
                     sql.Identifier(table))
    cursor.execute(query_for_func)
    data_by_attributes = cursor.fetchall()

    return data_by_attributes


@database_connection.connection_handler
def delete_question_db(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})

    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})


# def add_data(data, file_name, data_header):  # Z
#     return connection.write_data_to_file(data, file_name, data_header)


@database_connection.connection_handler
def add_data(cursor, col_list, value_list, table):
    query_for_func = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
                     sql.Identifier(table),
                     sql.SQL(', ').join(map(sql.Identifier, col_list)),
                     sql.SQL(', ').join(sql.Placeholder() * len(value_list)))
    cursor.execute(query_for_func, value_list)


# def update_data(data, file_name, data_header):  # Z
#     return connection.write_data_to_file(data, file_name, data_header, False)


@database_connection.connection_handler
def update_data(cursor, col_list, value_list, table, id_):
    query_for_func = sql.SQL('UPDATE {} SET ({}) = ({}) WHERE id = {}').format(
                     sql.Identifier(table),
                     sql.SQL(', ').join(map(sql.Identifier, col_list)),
                     sql.SQL(', ').join(sql.Placeholder() * len(value_list)),
                     sql.SQL(id_))
    cursor.execute(query_for_func, value_list)


@database_connection.connection_handler
def get_sorted_data(cursor, sort_by, direction):# N
    if direction == "asc":
        cursor.execute(
            sql.SQL("""SELECT
                id,
                submission_time,
                view_number, vote_number,
                title
                FROM question
                ORDER BY {sort_by} ASC LIMIT 5""").format(sort_by=sql.Identifier(sort_by)))
    elif direction == "desc":
        cursor.execute(
            sql.SQL("""SELECT
                        id,
                        submission_time,
                        view_number, vote_number,
                        title
                        FROM question
                        ORDER BY {sort_by} DESC LIMIT 5""").format(sort_by=sql.Identifier(sort_by)))
    data = cursor.fetchall()
    return data


def save_vote(file_name, question_id, vote_type, data_header, answer_id):  # Z
    existing_votes = connection.get_all_data_from_file(file_name)
    voted_id = question_id if answer_id == 'None' else answer_id
    for row in existing_votes:
        if row['id'] == voted_id:
            modifier = 1 if vote_type == 'up' else -1
            row['vote_number'] = str(int(row['vote_number']) + modifier) if row['vote_number'] else modifier
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
