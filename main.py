import os
import time
from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-production")

failed_attempts = {}

@app.route("/")
def Home():
    guessData = db.GetAllGuesses()
    return render_template("index.html", guesses=guessData)

@app.route("/login", methods=["GET", "POST"])
def Login():
    if session.get("username") is not None:
        return redirect("/")

    current_time = time.time()

    # Check if this browser session is currently locked
    locked_until = session.get("locked_until")
    if locked_until and current_time < locked_until:
        return render_template("login.html", locked_until=int(locked_until))

    # Clear expired lock
    if locked_until and current_time >= locked_until:
        session.pop("locked_until", None)

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username in failed_attempts:
            attempts = failed_attempts[username]
            if attempts["count"] >= 5 and current_time - attempts["last_attempt"] < 300:
                lock_time = int(attempts["last_attempt"] + 300)
                session["locked_until"] = lock_time
                return render_template("login.html", locked_until=lock_time)

        user = db.CheckLogin(username, password)
        if user:
            session.pop("locked_until", None)
            session["username"] = user["username"]
            session["id"] = user["id"]
            failed_attempts[username] = {"count": 0, "last_attempt": current_time}
            return redirect("/")

        if username not in failed_attempts:
            failed_attempts[username] = {"count": 1, "last_attempt": current_time}
        else:
            failed_attempts[username]["count"] += 1
            failed_attempts[username]["last_attempt"] = current_time

        # If they just hit the lockout threshold, activate overlay immediately
        if failed_attempts[username]["count"] >= 5:
            lock_time = int(current_time + 300)
            session["locked_until"] = lock_time
            return render_template("login.html", locked_until=lock_time)

        return render_template("login.html", error="Incorrect username or password.", locked_until=None)

    return render_template("login.html", locked_until=None)

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():
    if session.get("username") is not None:
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if db.RegisterUser(username, password):
            return redirect("/")

        return render_template("register.html", error="Registration failed. Check username, password, or duplicate account.")

    return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
def Add():
    if session.get("username") is None:
        return redirect("/")

    if request.method == "POST":
        user_id = session["id"]
        date = request.form["date"].strip()
        game = request.form["game"].strip()
        score = request.form["score"].strip()

        if db.AddGuess(user_id, date, game, score):
            return redirect("/")

        return render_template("add.html", error="Please enter a valid date, game, and score.")

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=False, port=5000)