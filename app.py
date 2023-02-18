from flask import Flask, render_template, request, session, jsonify
from boggle import Boggle


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret5678'


boggle_game = Boggle()



@app.route('/')
def homepage():
    """Display Homepage"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    timesplayed = session.get("timesplayed", 0)
    
    return render_template('homepage.html', board = board, highscore=highscore, timesplayed=timesplayed)

@app.route('/validate')
def validate():
    """Check if the word is a valid guess by checking if it is in dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/final-score', methods=["POST"])
def final_score():
    """Gives final score and updates high score"""
    score = int(request.json["score"])
    highscore = int(session.get("highscore", 0))
    timesplayed = session.get("timesplayed", 0)

    session["timesplayed"] = timesplayed + 1
    session["highscore"] = max(score, highscore)

    return jsonify(newHighScore = score > highscore)

