from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, send
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
      id = db.Column(db.Integer, primary_key=True, nullable=False)
      username = db.Column(db.String(80), unique=True, nullable=False)
      email = db.Column(db.String(120), unique=True, nullable=False)
      password_hash = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/lobby')
@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form.get('username-reg')
       email = request.form.get('Email-reg')
       password = request.form.get('password-reg')
       confirm_password = request.form.get('repet-pass')

       if password != confrim_password:
          flash('Password do not match')
          return redirect(url_for('register'))

          hash_pw = generate_password_hash(password)
          new_user = User(username=username, email=email, password=hash_pw)

       try:
          db.session.add(new_user)
          db.session.commit()
          return redirect(url_for('login'))

       except:
          db.session.rollback()
          flash('Username or Email already exist')
          return redirect(url_for('register'))

    return render_template(url_for('signup.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       username = request.form.get('username')
       password = request.form.get('email')

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
    socketio.emit('join_room_notification', data, room=data['room'])

if __name__ == "__main__":
    socketio.run(app, debug=True)
