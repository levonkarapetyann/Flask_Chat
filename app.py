from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
