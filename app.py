from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

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

@socketio.on('send')
def handle_send(data):
    app.logger.info("{} sent message to the room {}: {}".format(data['username'], data['room'], data['message']))
    socketio.emit('give_msg', data)


@socketio.on('join_room')
def handle_join_room(data):
    app.logger.info("{} joined the room: {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_notification', data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
