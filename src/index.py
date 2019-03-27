#!/usr/bin/env python3
from flask import Flask
import pandas
app = Flask(__name__)


@app.route("/")
def hello():
    return "dupa zbita"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
