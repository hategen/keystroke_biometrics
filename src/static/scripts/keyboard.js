import IOSocket from '../sockets.js'
import {getCookie} from './cookies.js'

const metricsSocket = new IOSocket();

const keyDowns = rxjs.fromEvent(document, 'keydown');
const keyUps = rxjs.fromEvent(document, 'keyup');

const keyActions = rxjs.merge(keyDowns, keyUps)

const compareEvents = (a, b) => a.type === b.type && a.key === b.key

const stream = keyActions
    .pipe(rxjs.operators.distinctUntilChanged(compareEvents), rxjs.operators.map(e => {
        return {
            type: e.type,
            key: e.key,
            timestamp: Date.now(),
            input: e.srcElement.name,
            login: getCookie('login')
        }
    }), rxjs.operators.bufferCount(30))

stream.subscribe((metrics) => {
    console.dir(metrics)
    metricsSocket.emitMetric(metrics)
});
