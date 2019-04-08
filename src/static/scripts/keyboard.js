import IOSocket from '../sockets.js'
import {getCookie} from './cookies.js'
import {processMetrics} from './metrics.js'

const metricsSocket = new IOSocket();

const keyDowns = rxjs.fromEvent(document, 'keydown');
const keyUps = rxjs.fromEvent(document, 'keyup');

const keyActions = rxjs.merge(keyDowns, keyUps)

const compareEvents = (a, b) => a.type === b.type && a.key === b.key

const stream = keyActions
    .pipe(rxjs.operators.distinctUntilChanged(compareEvents),
        rxjs.operators.filter(e=>![' ','Shift','Tab','Backspace'].includes(e.key)),
        rxjs.operators.map(e => {
        return {
            type: e.type,
            key: e.key.toLowerCase(),
            timestamp: Date.now(),
            input: e.srcElement.name,
            login: getCookie('login')
        }
    }), rxjs.operators.bufferCount(30))

stream.subscribe((metrics) => {
    console.dir(metrics);
    console.dir(processMetrics(metrics));

    metricsSocket.emitMetric(metrics)
});
