console.log('YO')

 const socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('response', (msg)=> {
       console.log(`RESPONSE: ${msg}`)
    });

    socket.emit('metric', {data: 'somedata'});