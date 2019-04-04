#!/usr/bin/env python3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import csv

app = Flask(__name__)
socketio = SocketIO(app)


def writeToCsv(batch):
    with open('metrics.csv', mode='a+') as csv_file:
        fieldnames = ['login', 'type', 'key', 'timestamp', 'input']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
        sniffer = csv.Sniffer()
        has_header = False
        line = csv_file.readline()

        if len(line) > 0:
            has_header = sniffer.has_header(line)

        if not has_header:
            writer.writeheader()

        for element in batch:
            writer.writerow(element)


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
    app.logger.debug(type(metricData))
    app.logger.debug('metric: ' + str(metricData))
    writeToCsv(metricData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
