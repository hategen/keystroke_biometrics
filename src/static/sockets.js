export default class IOSocket {
    constructor(domain = document.domain, port = location.port) {
        this.socket = io.connect(`http://${document.domain}:${location.port}`);
    }

    disconnect() {
        this.socket.disconnect()
    }

    emitMetric(metric = {}) {
        this.socket.emit('metric', metric);
    }
}


