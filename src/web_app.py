import logging
import os
import sys

logging.basicConfig(
    level=logging.WARNING,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('garmindb.log', mode='w')
    ],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


import markdown
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

from fetch_and_suggest.main import fetch_and_generate_suggestions
from config import dummy_response

DUMMY_RESPONSE = True


@app.route("/health")
def health():
    return "OK", 200

@app.route("/")
def hello_world():

    if DUMMY_RESPONSE:
        recent_runs, suggested_next_run = dummy_response["recent_runs"], dummy_response["suggested_next_run"]
    else:
        recent_runs, suggested_next_run = fetch_and_generate_suggestions()

    return render_template(
        'index.html',
        recent_runs=recent_runs,
        suggested_next_run=markdown.markdown(suggested_next_run, extensions=['nl2br']))


if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")
