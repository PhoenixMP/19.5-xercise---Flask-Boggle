
from boggle import Boggle
from flask import Flask, request, render_template, jsonify, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
boggle_game = Boggle()


@app.route('/')
def boggle_home():
    """Show boggle homepage with board and score."""

    board = boggle_game.make_board()
    session['board'] = board
    session['score'] = session.get('score', 0)
    if session['score'] != 0:
        message = f"Your High-Score is {session['score']}"
    else:
        message = f"Get ready to rack up some points!"

    return render_template("index.html", board=board, message=message)


@app.route('/guess')
def process_guess():
    """Process guess and send message to front-end."""

    word = request.args['guess']
    board = session['board']
    response = boggle_game.check_valid_word(board, word.lower())
    return jsonify({'result': response})


@app.route('/score', methods=['POST'])
def process_score():
    """Acquire high-score from front-end, increase round count."""
    score = request.json['score']
    session['score'] = session.get('score', 0) + score
    session['count'] = session.get('count', 0) + 1
    response = {'score': session['score'], 'count': session['count']}
    return jsonify({'result': response})
