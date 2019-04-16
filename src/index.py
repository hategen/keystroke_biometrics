#!/usr/bin/env python3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import csv
import pandas as pd

app = Flask(__name__)
socketio = SocketIO(app)

csvPath = 'datasets/metrics.csv'


def writeToCsv(batch):
    has_header = False
    fieldnames = ['login', 'type', 'key', 'timestamp', 'input', 'keypressDuration', 'keyDownTimestamp',
                  'keyUpTimestamp']
    try:
        metrics = pd.read_csv(csvPath)
    except:
        print('Create new file '+csvPath)
        metrics = pd.DataFrame(columns=fieldnames)
    metrics.append(pd.DataFrame(batch), ignore_index=True)
    metrics.to_csv(csvPath)
    # with open('metrics.csv', mode='r') as csv_file:
    #     line = csv_file.readline()
    #     print(line)
    #     sniffer = csv.Sniffer()
    #     if len(line) > 0:
    #         has_header = sniffer.has_header(line)

    # with open('metrics.csv', mode='a+') as csv_file:

    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')

    #     if has_header == False:
    #         writer.writeheader()

    #     for element in batch:
    #         writer.writerow(element)


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
