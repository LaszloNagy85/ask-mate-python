from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)









if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
