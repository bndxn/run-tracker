import os

import markdown
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

from main import main


@app.route("/")
def hello_world():
    recent_runs, suggested_next_run = main()

    return render_template(
        'index.html',
        recent_runs=recent_runs,
        suggested_next_run=markdown.markdown(suggested_next_run, extensions=['nl2br']))


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
