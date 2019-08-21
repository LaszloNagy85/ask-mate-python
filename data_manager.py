import database_connection
from psycopg2 import sql
import bcrypt


@database_connection.connection_handler
def get_all_data(cursor, table):
    query_for_func = sql.SQL('SELECT * FROM {}').format(
                     sql.Identifier(table))
    cursor.execute(query_for_func)
    all_data = cursor.fetchall()

    return all_data


# if the col_value is a string, use "'col_value'
# use it only on question, answer, comment tables!
@database_connection.connection_handler
def get_columns_by_attribute(cursor, col_list, table, col_name, col_value):
    query_for_func = sql.SQL('SELECT {} FROM {} WHERE {} = {} ORDER BY submission_time').format(
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


# copy of get_columns_by_attribute without order
@database_connection.connection_handler
def get_filtered_data(cursor, col_list, table, col_name, col_value):
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


@database_connection.connection_handler
def search_question(cursor, search_input):
    query_for_func = sql.SQL("""SELECT
                                id,
                                submission_time,
                                vote_number,
                                view_number,
                                title,
                                message
                                FROM question
                                WHERE LOWER(message) LIKE LOWER({search}) OR
                                LOWER(title) LIKE LOWER({search})
                                ORDER BY submission_time DESC""").format(search=sql.SQL(f"'%{search_input}%'"))
    cursor.execute(query_for_func)
    data = cursor.fetchall()
    return data


@database_connection.connection_handler
def search_answer(cursor, search_input):
    query_for_func = sql.SQL("""SELECT
                                answer.id,
                                answer.submission_time,
                                answer.vote_number,
                                answer.question_id,
                                answer.message,
                                question.title
                                FROM answer
                                INNER JOIN question
                                    ON answer.question_id = question.id
                                WHERE LOWER(answer.message) LIKE LOWER({})
                                ORDER BY answer.submission_time DESC""").format(sql.SQL(f"'%{search_input}%'"))
    cursor.execute(query_for_func)
    data = cursor.fetchall()
    return data


def highlight(data, search_input):
    for row in data:
        startspan = '<span class="highlight">'
        endspan = '</span>'
        message = row['message']
        index = 0

        while index < len(message):
            index = message.lower().find(search_input.lower(), index)
            if index == -1:
                break
            message = message[:index] + startspan + message[index: index + len(search_input)] \
                + endspan + message[index + len(search_input):]
            index += (len(startspan) + len(search_input) + len(endspan))
        row['message'] = message

        title = row['title']
        index = 0

        while index < len(title):
            index = title.lower().find(search_input.lower(), index)
            if index == -1:
                break
            title = title[:index] + startspan + title[index: index + len(search_input)] \
                + endspan + title[index + len(search_input):]
            index += (len(startspan) + len(search_input) + len(endspan))
        row['title'] = title
    return data


@database_connection.connection_handler
def delete_answer_db(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer)s;
                    """,
                   {'answer': answer_id})


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


@database_connection.connection_handler
def add_data(cursor, col_list, value_list, table):
    query_for_func = sql.SQL('INSERT INTO {} ({}) VALUES ({}) RETURNING id').format(
                     sql.Identifier(table),
                     sql.SQL(', ').join(map(sql.Identifier, col_list)),
                     sql.SQL(', ').join(sql.Placeholder() * len(value_list)))

    cursor.execute(query_for_func, value_list)
    id_ = cursor.fetchone()

    return id_['id']


@database_connection.connection_handler
def update_data(cursor, col_list, value_list, table, id_):
    query_for_func = sql.SQL('UPDATE {} SET ({} ) = ({}) WHERE id = {}').format(
                     sql.Identifier(table),
                     sql.SQL(', ').join(map(sql.Identifier, col_list)),
                     sql.SQL(', ').join(sql.Placeholder() * len(value_list)),
                     sql.SQL(id_))
    cursor.execute(query_for_func, value_list)


@database_connection.connection_handler
def get_sorted_data(cursor, sort_by, direction):
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


@database_connection.connection_handler
def get_all_sorted_questions(cursor, sort_by, direction):
    if direction == "asc":
        cursor.execute(
            sql.SQL("""SELECT
                id,
                submission_time,
                view_number, vote_number,
                title
                FROM question
                ORDER BY {sort_by} ASC""").format(sort_by=sql.Identifier(sort_by)))
    elif direction == "desc":
        cursor.execute(
            sql.SQL("""SELECT
                        id,
                        submission_time,
                        view_number, vote_number,
                        title
                        FROM question
                        ORDER BY {sort_by} DESC""").format(sort_by=sql.Identifier(sort_by)))
    data = cursor.fetchall()
    return data


@database_connection.connection_handler
def save_vote(cursor, id_, vote_type, table):
    vote_number = get_columns_by_attribute(['vote_number'], table, 'id', id_)['vote_number']
    if vote_type == 'up':
        vote_number += 1
    elif vote_type == 'down':
        vote_number -= 1
    update_data(['vote_number', 'id'], [vote_number, id_], table, id_)


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


@database_connection.connection_handler
def delete_comment_db(cursor, comment_id):

    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'question_id': comment_id})


@database_connection.connection_handler
def delete_from_db(cursor, id_, table):

    cursor.execute(
            sql.SQL('DELETE FROM {} WHERE id = %(id)s').format(sql.Identifier(table)), {'id': id_})


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_connection.connection_handler
def get_data_from_user_db(cursor, col_list, table, col_name, col_value):
    query_for_func = sql.SQL('SELECT {} FROM {} WHERE {} = {}').format(
        sql.SQL(', ').join(map(sql.Identifier, col_list)),
        sql.Identifier(table),
        sql.Identifier(col_name),
        sql.SQL(col_value))
    cursor.execute(query_for_func)

    if col_name == 'id':
        data = cursor.fetchone()
    elif col_name == 'name':
        data = cursor.fetchone()
    else:
        data = cursor.fetchall()

    return data
