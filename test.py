from flask import Flask, render_template, request, redirect, url_for

import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def route_index():
    # all_questions = data_manager.get_all_data('question')
    # all_answers = data_manager.get_all_data('answer')
    #
    # question_titles = data_manager.get_all_data_of_one_type('title', 'question')
    # question_messages = data_manager.get_all_data_of_one_type('message', 'question')
    # answer_messages = data_manager.get_all_data_of_one_type('message', 'answer')
    questions = data_manager.get_all_data('test')
    answers = data_manager.get_all_data('test_answers')

    return render_template('test.html',
                           questions=questions,
                           answers=answers)

# @app.route('/question/<question_id>', methods=['POST'])
# def route_vote():
#     if request.method == 'POST':
#         if 'votedown' in request.form:


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager.get_selected_data('test', question_id, 'id')  # note to self: reconsider this!
    answers = data_manager.get_selected_data('test_answers', question_id, 'question_id')

    data_manager.convert_readable_dates(question)
    data_manager.convert_readable_dates(answers)

    return render_template('question.html',
                           question=question[0],
                           answers=answers,
                           )


@app.route('/question/<question_id>/delete/', methods=['POST'])
def route_delete_question(question_id):
    if request.method == 'POST':
        remaining_questions, remaining_answers = data_manager.delete_question(question_id)
        connection.write_remaining_data_to_file(remaining_questions, 'test', connection.DATA_HEADER_QUESTION)
        connection.write_remaining_data_to_file(remaining_answers, 'test_answers', connection.DATA_HEADER_ANSWER)

        return redirect('/')


@app.route('/answer/<answer_id>/delete/', methods=['POST'])
def route_delete_answer(answer_id):
    if request.method == 'POST':
        question_id = data_manager.get_selected_data('test_answers', answer_id, 'id')[0]['question_id']
        remaining_answers = data_manager.delete_answer(answer_id, 'id')
        connection.write_remaining_data_to_file(remaining_answers, 'test_answers', connection.DATA_HEADER_ANSWER)

    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=False,
    )
