from flask import Flask, render_template, request, redirect, url_for

import data_manager
import util
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"


QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
SORT_OPTIONS = ['submission_time', 'view_number', 'vote_number', 'title']
SORT_TITLES = ['Submission time', 'View number', 'Vote number', 'Title']


@app.route('/question/<question_id>/')
def route_question(question_id):
    question = data_manager.get_selected_data('question', question_id, 'id')
    answers = data_manager.get_selected_data('answer', question_id, 'question_id')

    data_manager.convert_readable_dates(question)
    data_manager.convert_readable_dates(answers)

    return render_template('question.html',
                           question=question[0],
                           answers=answers,
                           form_url=url_for('route_new_answer', question_id=question_id),
                           page_title='Display a question',
                           button_title='Save new answer',
                           )


@app.route('/question/counted/<question_id>/')
def route_question_counted(question_id):
    question = data_manager.get_selected_data('question', question_id, 'id')
    url = str(request.referrer)
    if url == 'http://127.0.0.1:8000/' or '?sort_by=' in url:
        view_number = int(question[0]['view_number'])
        view_number += 1
        question[0]['view_number'] = view_number
        data_manager.update_data(question[0], 'question', DATA_HEADER_QUESTION)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def route_new_answer(question_id):
    new_answer_id = data_manager.generate_id('answer')
    submission_time = util.get_epoch()
    image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

    new_answer = {
        'id': new_answer_id,
        'submission_time': submission_time,
        'vote_number': '0',
        'question_id': question_id,
        'message': request.form.get('message'),
        'image': image.filename if image else None,
    }

    data_manager.add_data(new_answer, 'answer', DATA_HEADER_ANSWER)

    return redirect(f'/question/{question_id}')


@app.route('/')
def route_list_of_questions():
    sort_by = 'submission_time'
    direction = 'desc'
    if 'sort_by' in request.args:
        sort_by = request.args.get('sort_by')
    if 'direction' in request.args:
        direction = request.args.get('direction')
    data = data_manager.get_sorted_data(sort_by, direction)
    answers = data_manager.get_data_by_attributes(['id', 'question_id', 'message'], 'answer')

    return render_template('list.html',
                           questions=data,
                           answers=answers,
                           sort_by=sort_by,
                           direction=direction,
                           sort_options=SORT_OPTIONS,
                           sort_titles=SORT_TITLES,
                           directions=['Ascending', 'Descending'],
                           reverse_options=['asc', 'desc'])


@app.route('/add-question', methods=['GET', 'POST'])
def route_question_add():
    generated_id = data_manager.generate_id('question')
    if request.method == 'POST':
        image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

        question = {
            'id': generated_id,
            'submission_time': util.get_epoch(),
            'view_number': '0',
            'vote_number': '0',
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': image.filename if image else None,
        }

        data_manager.add_data(question, 'question', DATA_HEADER_QUESTION)
        return redirect(f'/question/{generated_id}')

    return render_template('add-question.html',
                           question=[{}],
                           form_url=url_for('route_question_add'),
                           page_title='Ask a question',
                           button_title='Save question',
                           )


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_update(question_id):
    FIRST = 0
    if request.method == 'POST':
        stored_data = data_manager.get_selected_data('question', question_id, 'id')

        image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

        question = {
            'id': question_id,
            'submission_time': util.get_epoch(),
            'view_number': stored_data[FIRST]['view_number'],
            'vote_number': stored_data[FIRST]['vote_number'],
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': image.filename if image else stored_data[FIRST]['image']
        }

        data_manager.update_data(question, 'question', DATA_HEADER_QUESTION)
        return redirect(f'/question/{question_id}')

    question = data_manager.get_selected_data('question', question_id, 'id')

    return render_template('add-question.html',
                           question=question,
                           form_url=url_for('route_question_update', question_id=question_id),
                           page_title='Edit a question',
                           button_title='Update question',
                           )


@app.route('/vote/<file_name>/<question_id>/<vote_type>/<answer_id>')
def vote(file_name, question_id, vote_type, answer_id):
    header = DATA_HEADER_QUESTION if answer_id == 'None' else DATA_HEADER_ANSWER
    data_manager.save_vote(file_name, question_id, vote_type, header, answer_id)
    return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/delete/', methods=['POST'])
def route_delete_question(question_id):
    if request.method == 'POST':

        question = data_manager.get_columns_by_attribute(['image'], 'question', 'id', question_id)
        answers = data_manager.get_columns_by_attribute(['image'], 'answer', 'question_id', question_id)

        image_filenames = [question['image']] + [answer['image'] for answer in answers]
        data_manager.delete_image(image_filenames, app.config['UPLOAD_FOLDER'])

        data_manager.delete_question_db(question_id)

        return redirect('/')


@app.route('/answer/<answer_id>/delete/', methods=['POST'])
def route_delete_answer(answer_id):
    if request.method == 'POST':
        data_of_answer = data_manager.get_columns_by_attribute(['question_id', 'image'], 'answer', 'answer_id', answer_id)
        question_id = data_of_answer['question_id']

        if data_of_answer['image']:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data_of_answer['image']))

        data_manager.delete_answer_db(answer_id)

    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        port=8000,
        debug=False,
    )
