#!/usr/bin/env python3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging
from logging import Formatter

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def hello():
    return render_template('index.html')


@socketio.on('connect', namespace='/metrics')
def connect():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    emit('response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/metrics')
def disconnect():
    app.logger.info('Disconnected')
    emit('response', {'data': 'Disconnected'})


@socketio.on('metric', namespace='/metrics')
def metric(message):
    emit('response', {'data': 'metric'})


if __name__ == '__main__':
    # Setup the logger
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    app.logger.error('Starting app...')
    app.run(host='0.0.0.0', debug=True)
