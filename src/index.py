#!/usr/bin/env python3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pandas as pd
import os

app = Flask(__name__)
socketio = SocketIO(app)




def writeToCsv(batch):
    csvPath = batch[0]['login']+'.csv'

    if (os.path.isfile(csvPath)):
        metrics = pd.read_csv(csvPath).append(
            pd.DataFrame(batch), ignore_index=True)
    else:
        metrics = pd.DataFrame(batch)

    metrics.to_csv(csvPath, index=False)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/playground")
def playground():
    return render_template('playground.html', title='Playground')


@socketio.on('connect')
def connect():
    emit('response', {'data': 'Connected'})


@socketio.on('disconnect')
def disconnect():
    print('Disconnected')


@socketio.on('metric')
def metric(metricData, methods=['GET', 'POST']):
    # app.logger.debug(type(metricData))
    # app.logger.debug('metric: ' + str(metricData))
    writeToCsv(metricData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
