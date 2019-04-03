import IOSocket from '../sockets.js'
import {getCookie} from './cookies.js'

const metricsSocket = new IOSocket();

const keyDowns = rxjs.fromEvent(document, 'keydown');
const keyUps = rxjs.fromEvent(document, 'keyup');

const keyActions = rxjs.merge(keyDowns, keyUps)

const compareEvents = (a, b) => a.type === b.type && a.key === b.key

const stream = keyActions.pipe(rxjs.operators.distinctUntilChanged(compareEvents))

stream.subscribe((e) => {
    const metric = {
        type: e.type,
        key: e.key,
        timestamp: Date.now(),
        input: e.srcElement.name,
        login: getCookie('login')
    }
    console.dir(metric)
    metricsSocket.emitMetric(metric)
});
