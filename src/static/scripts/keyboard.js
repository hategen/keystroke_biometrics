import IOSocket from '../sockets.js'
import {getCookie} from './cookies.js'
import {processMetrics} from './metrics.js'

const metricsSocket = new IOSocket();

const getKeyActionsStream = element => {
    const keyDowns$ = rxjs.fromEvent(element, 'keydown');
    const keyUps$ = rxjs.fromEvent(element, 'keyup');
    const keyActions$ = rxjs.merge(keyDowns$, keyUps$)

    return keyActions$;
}

const getClickStream = msg => selector => {
    const element = document.querySelector(selector);

    if (!element) {
        throw Error(`${selector} element not found!`);
    }

    const start$ = rxjs
        .fromEvent(element, 'click');
    console.log(msg, element);

    return start$;
}

const start = getClickStream('Starting keydown and keyup logging on');
const stop = getClickStream('Stopping keydown and keyup logging on');

const compareEvents = (a, b) => a.type === b.type && a.key === b.key

const getMetricsStream = (keyActionStream$, start$, stop$) => {

    const metricsStream$ = keyActionStream$.pipe(rxjs.operators.distinctUntilChanged(compareEvents),
        rxjs.operators.filter(e => !['Shift', 'Tab', 'Backspace'].includes(e.key)),
        rxjs.operators.map(e => {
            return {
                type: e.type,
                key: e.key.toLowerCase(),
                timestamp: Date.now(),
                input: e.srcElement.name,
                login: getCookie('login')
            }
        }),
        rxjs.operators.bufferToggle(start$, () => stop$));
    return metricsStream$;
}

export function attachKeylogger(inputSelector, startSelector, stopSelector) {

    const element = document.querySelector(inputSelector);

    if (!element) {
        throw Error(`${inputSelector} element not found!`);
    }

    const $keyStream = getKeyActionsStream(element);
    const start$ = start(startSelector);
    const stop$ = stop(stopSelector);

    const metricsStream$ = getMetricsStream($keyStream, start$, stop$);

    metricsStream$.subscribe((metrics) => {
        const processedMetrics = processMetrics(metrics)
        console.dir(metrics);
        console.dir(processedMetrics);

        if (processedMetrics.length) {
            metricsSocket.emitMetric(processedMetrics)
        }
    });
}