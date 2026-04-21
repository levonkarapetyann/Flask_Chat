from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_socketio import SocketIO, join_room, send
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'very very secret key'


db = SQLAlchemy(app)

class User(db.Model):
      id = db.Column(db.Integer, primary_key=True, nullable=False)
      username = db.Column(db.String(80), unique=True, nullable=False)
      email = db.Column(db.String(120), unique=True, nullable=False)
      password_hash = db.Column(db.String(120), nullable=False)
      date = db.Column(db.DateTime, default=datetime.utcnow)


      def __repr__(self):
          return f"<profiles {self.id}>"

@app.route('/lobby')
@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form.get('username_reg')
       email = request.form.get('Email-reg')
       password = request.form.get('password-reg')
       confirm_password = request.form.get('repet-pass')

       if password != confirm_password:
          flash('Password do not match')
          return redirect(url_for('register'))

       hash_pw = generate_password_hash(password)
       new_user = User(username=username, email=email, password_hash=hash_pw)

       try:
          db.session.add(new_user)
          db.session.commit()
          return redirect(url_for('login'))

       except Exception as e:
          db.session.rollback()
          print(f"Erro: {e}")
          flash('Username or Email already exist')
          return redirect(url_for('register'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       username = request.form.get('username')
       password = request.form.get('password')


       found_user = User.query.filter_by(username=username).first()

       if found_user and check_password_hash(found_user.password_hash, password):
           flash("Login Succesfull!")
           return redirect(url_for('chat'))
       else:
           flash("Username or password incorrect...")
           return redirect(url_for('login'))

    return render_template('/main.html')
@app.route('/chat')
def chat():
    pass


if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    socketio.run(app, debug=True, port=5001)
