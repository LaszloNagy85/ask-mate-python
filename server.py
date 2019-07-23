from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route('/question/<question_id>')
def route_question(question_id=None):
    question = data_manager.get_selected_data('question', question_id, 'id')[0]
    answers = data_manager.get_selected_data('answer', question_id, 'question_id')
    print(question)
    print(answers)

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           )


if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
