from flask import Flask, render_template, request, redirect, url_for

import data_manager
import util
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"


QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
COMMENT = ['id', 'question_id', 'answer_id', 'message', 'submission_time', 'edited_count']
SORT_OPTIONS = ['submission_time', 'view_number', 'vote_number', 'title']
SORT_TITLES = ['Submission time', 'View number', 'Vote number', 'Title']


@app.route('/question/<question_id>/')
def route_question(question_id):
    question = data_manager.get_columns_by_attribute(QUESTION, 'question', 'id', question_id)
    answers = data_manager.get_columns_by_attribute(ANSWER, 'answer', 'question_id', question_id)
    comment = data_manager.get_columns_by_attribute(COMMENT, 'comment', 'question_id', question_id)

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           comment=comment,
                           form_url=url_for('route_new_answer', question_id=question_id),
                           page_title='Display a question',
                           button_title='Save new answer',
                           stored_answer='',
                           legend='Write new answer')


@app.route('/question/counted/<question_id>/')
def route_question_counted(question_id):
    question = data_manager.get_columns_by_attribute(['view_number'], 'question', 'id', question_id)
    url = str(request.referrer)
    if url == 'http://127.0.0.1:8000/' or url == 'http://127.0.0.1:8000/list' or '?sort_by=' in url:
        view_number = int(question['view_number']) + 1
        data_manager.update_data(['view_number', 'id'], [view_number, question_id], 'question', question_id)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def route_new_answer(question_id):
    image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

    new_answer = {
        'submission_time': util.get_timestamp(),
        'vote_number': '0',
        'question_id': question_id,
        'message': request.form.get('message'),
        'image': image.filename if image else None,
    }

    data_manager.add_data(new_answer.keys(), list(new_answer.values()), 'answer')

    return redirect(f'/question/{question_id}')


@app.route('/')
def route_list_of_questions():
    ORDER = 4
    DIRECTION = 2
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
                           reverse_options=['asc', 'desc'],
                           order_by=ORDER,
                           order=DIRECTION,
                           form_action='/',
                           button_action='/list',
                           button_text='Show all')


@app.route('/add-question', methods=['GET', 'POST'])
def route_question_add():
    if request.method == 'POST':
        image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

        question = {
            'submission_time': util.get_timestamp(),
            'view_number': '0',
            'vote_number': '0',
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': image.filename if image else None,
        }

        generated_id = data_manager.add_data(question.keys(), list(question.values()), 'question')

        return redirect(f'/question/{generated_id}')

    return render_template('add-question.html',
                           question={},
                           form_url=url_for('route_question_add'),
                           page_title='Ask a question',
                           button_title='Save question',
                           )


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_update(question_id):
    if request.method == 'POST':
        stored_data = data_manager.get_columns_by_attribute(QUESTION, 'question', 'id', question_id)

        image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

        question = {
            'submission_time': util.get_timestamp(),
            'view_number': stored_data['view_number'],
            'vote_number': stored_data['vote_number'],
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': image.filename if image else stored_data['image']
        }

        data_manager.update_data(['title', 'message'], [question['title'], question['message']], 'question', question_id)
        return redirect(f'/question/{question_id}')

    question = data_manager.get_columns_by_attribute(QUESTION, 'question', 'id', question_id)

    return render_template('add-question.html',
                           question=question,
                           form_url=url_for('route_question_update', question_id=question_id),
                           page_title='Edit question',
                           button_title='Update question',
                           )


@app.route('/vote/<question_id>/<vote_type>/<answer_id>')
def vote(question_id, vote_type, answer_id):
    if answer_id == 'None':
        table = 'question'
        id_ = question_id
    else:
        table = 'answer'
        id_ = answer_id

    data_manager.save_vote(id_, vote_type, table)
    return redirect(f'/question/{question_id}')


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
        data_of_answer = data_manager.get_columns_by_attribute(['question_id', 'image'], 'answer', 'id', answer_id)
        question_id = data_of_answer['question_id']

        if data_of_answer['image']:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data_of_answer['image']))

        data_manager.delete_answer_db(answer_id)

    return redirect(f'/question/{question_id}')


@app.route('/list')
def all_questions():
    ORDER = 4
    DIRECTION = 2
    sort_by = 'submission_time'
    direction = 'desc'
    if 'sort_by' in request.args:
        sort_by = request.args.get('sort_by')
    if 'direction' in request.args:
        direction = request.args.get('direction')
    data = data_manager.get_all_sorted_questions(sort_by, direction)
    answers = data_manager.get_data_by_attributes(['id', 'question_id', 'message'], 'answer')

    return render_template('list.html',
                           questions=data,
                           answers=answers,
                           sort_by=sort_by,
                           direction=direction,
                           sort_options=SORT_OPTIONS,
                           sort_titles=SORT_TITLES,
                           directions=['Ascending', 'Descending'],
                           reverse_options=['asc', 'desc'],
                           order_by=ORDER,
                           order=DIRECTION,
                           form_action='/list',
                           button_action='/',
                           button_text='Show less')


@app.route('/question/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def route_answer_update(question_id, answer_id):
    if request.method == 'POST':
        stored_data = data_manager.get_columns_by_attribute(['image'], 'answer', 'id', answer_id)

        image = data_manager.save_image(app.config['UPLOAD_FOLDER'], request.files)

        answer = {
            'submission_time': util.get_timestamp(),
            'message': request.form.get('message'),
            'image': image.filename if image else stored_data['image']
        }

        data_manager.update_data(['message', 'submission_time', 'image'],
                                 [answer['message'], answer['submission_time'],
                                 answer['image']], 'answer',
                                 answer_id)
        return redirect(f'/question/{question_id}#{answer_id}')

    question = data_manager.get_columns_by_attribute(QUESTION, 'question', 'id', question_id)
    answers = data_manager.get_columns_by_attribute(ANSWER, 'answer', 'question_id', question_id)
    answer = data_manager.get_columns_by_attribute(['message', 'image'], 'answer', 'id', answer_id)

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           page_title='Edit answer',
                           button_title='Update answer',
                           stored_answer=answer['message'],
                           legend='Edit answer'
                           )


@app.route('/question/<question_id>/new_comment', methods=['POST'])
def route_new_question_comment(question_id):

    new_comment = {
        'question_id': question_id,
        'message': request.form.get("message"),
        'submission_time': util.get_timestamp(),
        'edited_count': 0,
    }

    data_manager.add_data(new_comment.keys(), list(new_comment.values()), 'comment')

    return redirect('/question/<question_id>')


@app.route('/answer/<answer_id>/new_answer', methods='POST')
def route_new_answer_comment(answer_id):
    question_id = data_manager.get_columns_by_attribute('question_id', 'answer', 'answer_id', answer_id)

    new_comment = {
        'question_id': question_id,
        'answer_id': answer_id,
        'message': request.form.get('message'),
        'submission_time': util.get_timestamp(),
        'edited_count': 0
    }
    data_manager.add_data(new_comment.keys(), list(new_comment.values()), 'comment')

    return redirect('/question/<question_id>')


if __name__ == '__main__':
    app.run(
        port=8000,
        debug=False,
    )
