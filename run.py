import subprocess
import gevent

from flask import Flask
from flask_socketio import SocketIO
from flask import render_template

__author__ = 'BonfaceKilz'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app)


def background_thread(socket_obj):
    def run_process(cmd):
        socket_obj.emit('console-log',
                        {'data': f"{cmd}\n"})
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True)
        for c in iter(lambda: process.stdout.read(1), b''):
            socket_obj.emit('console-log',
                            {'data': c.decode('utf-8')})
            socket_obj.sleep(0.01)
        socket_obj.emit("console-log",
                        {'data': "DONE"})
    gevent.joinall(
        [gevent.spawn(run_process, "guix pull --dry-run")])


@socketio.on('gemma')
def gemma():
    socketio.start_background_task(background_thread, socketio)


@app.route('/')
def render_large_template():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
