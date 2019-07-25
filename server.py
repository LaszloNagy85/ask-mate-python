from flask import Flask, render_template, request, redirect, url_for

import data_manager
import util
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"


DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
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
    if str(request.referrer) == 'http://127.0.0.1:8000/':
        view_number = int(question[0]['view_number'])
        view_number += 1
        question[0]['view_number'] = view_number
        data_manager.update_data(question[0], 'question', DATA_HEADER_QUESTION)

    return redirect(f'/question/{question_id}')



@app.route('/question/<question_id>/new-answer', methods=['POST'])
def route_new_answer(question_id):
    new_answer_id = data_manager.generate_id('answer')
    submission_time = util.get_epoch()
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != "":
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    else:
        image = ''

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


@app.route('/', methods=['GET', 'POST'])
def route_list_of_questions():
    sort_by = 'submission_time'
    direction = 'True'
    if 'sort_by' in request.args:
        sort_by = request.args.get('sort_by')
    if 'direction' in request.args:
        direction = request.args.get('direction')
    data = data_manager.get_sorted_data('question', sort_by, direction)
    data = data_manager.get_dict_of_specific_types(['id', 'title'], data)
    return render_template('list.html',
                           data=data,
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
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "":
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        else:
            image = ''

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
        if request.method == 'POST':
            if 'image' in request.files:
                image = request.files['image']
                if image.filename != "":
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            else:
                image = ''

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


if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
