console.log('YO')

window.addEventListener('load',()=>{
const socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('response', (msg) => {
        console.log(`RESPONSE: ${msg}`);
    });

    socket.emit('metric', { data: 'somedata' });
})
