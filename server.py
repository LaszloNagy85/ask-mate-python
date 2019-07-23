from flask import Flask, render_template, request, redirect, url_for

import data_manager
import util

app = Flask(__name__)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager.get_selected_data('question', question_id, 'id')  # note to self: reconsider this!
    answers = data_manager.get_selected_data('answer', question_id, 'question_id')

    data_manager.convert_readable_dates(question)
    data_manager.convert_readable_dates(answers)

    print(question)  # for testing, delete it later!
    print(answers)  # for testing, delete it later!

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           )


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def route_new_answer(question_id):
    new_answer_id = data_manager.generate_id('answer')
    submission_time = util.get_epoch()

    modified_answer = {
        'id': new_answer_id,
        'submission_time': submission_time,
        'vote_number': '0',
        'question_id': question_id,
        'message': request.form.get('message'),
        'image': '',  # will be modified later
    }

    print(modified_answer)  # just for check until there is an export data function
    #  call export data function comes here
    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
