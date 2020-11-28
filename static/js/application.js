$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.emit('gemma');
    socket.on('console-log', function(msg) {
        console.log("Received message: " + msg.data);
        $('#log').append('<p>' + msg.data + '</p');
    });
});
