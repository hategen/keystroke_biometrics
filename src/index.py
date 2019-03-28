#!/usr/bin/env python3
import pandas
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    emit('response', {'data': 'Connected'})


@socketio.on('disconnect')
def disconnect():
    print('Disconnected')


@socketio.on('metric')
def metric(json, methods=['GET', 'POST']):
    app.logger.debug('metric: ' + str(json))
    socketio.emit('response', json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
