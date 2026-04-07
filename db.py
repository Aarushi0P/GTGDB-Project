import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():

    # Connect to the database and return the connection object
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row

    return db

def GetAllGuesses():

    # Connect, query all guesses and then return the data
    db = GetDB()
    guesses = db.execute("SELECT Guesses.date, Guesses.score, Guesses.game, Users.username FROM Guesses JOIN Users ON Guesses.user_id = Users.id").fetchall()
    db.close()
    return guesses