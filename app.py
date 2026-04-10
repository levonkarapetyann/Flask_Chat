from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

@app.route('/lobby')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
         return render_template('index.html')

@socketio.on('join_room')
def handle_join_room(data):
    app.logger.info("{} joined the room: {}".format(data['username'], data['room']))

if __name__ == "__main__":
    socketio.run(app, debug=True)
