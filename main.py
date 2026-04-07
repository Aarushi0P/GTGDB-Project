from flask import Flask, render_template, request, session, redirect, url_for
import db

app = Flask(__name__)
app.secret_key = "gtg_secret_key_123" # Change this for better security

@app.route("/")
def Home():
    guessData = db.GetAllGuesses()
    return render_template("index.html", guesses=guessData)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
