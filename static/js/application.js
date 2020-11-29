$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var term = new Terminal();
    term.open(document.getElementById('log'));
    // hide cursor:
    term.write('\x1b[?25I]')
    term.write('Hello from \x1B[1;3;31mGenenetwork\x1B[0m \n\r');
    socket.emit('gemma');

    socket.on('console-log', function(msg) {
        console.log("Received message: " + msg.data);
        term.write(msg.data);
    });
});
