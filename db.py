import re
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def GetDB():
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row
    return db


def GetAllGuesses():
    db = GetDB()
    guesses = db.execute("""
        SELECT Guesses.date, Guesses.score, Guesses.game, Users.username
        FROM Guesses
        JOIN Users ON Guesses.user_id = Users.id
        ORDER BY date DESC
    """).fetchall()
    db.close()
    return guesses


def CheckLogin(username, password):
    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()
    db.close()

    if user is not None and check_password_hash(user["password"], password):
        return user

    return None


def RegisterUser(username, password):
    if username is None or password is None:
        return False

    username = username.strip()
    password = password.strip()

    if username == "" or password == "":
        return False

    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,20}", username):
        return False

    if len(password) < 8:
        return False

    db = GetDB()
    existing_user = db.execute("SELECT id FROM Users WHERE username=?", (username,)).fetchone()
    if existing_user:
        db.close()
        return False

    password_hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, password_hash))
    db.commit()
    db.close()
    return True


def AddGuess(user_id, date, game, score):
    if user_id is None or date is None or game is None or score is None:
        return False

    date = date.strip()
    game = game.strip()
    score = str(score).strip()

    if date == "" or game == "" or score == "":
        return False

    if len(game) > 100:
        return False

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False

    try:
        score_int = int(score)
        if score_int < 0 or score_int > 100:
            return False
    except ValueError:
        return False

    db = GetDB()
    db.execute(
        "INSERT INTO Guesses(user_id, date, game, score) VALUES (?, ?, ?, ?)",
        (user_id, date, game, score_int)
    )
    db.commit()
    db.close()
    return True