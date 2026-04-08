import hashlib
import sqlite3


def GetDB():

    # Connect to the database and return the connection object
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row

    return db

def GetAllGuesses():

    # Connect, query all guesses and then return the data
    db = GetDB()
    guesses = db.execute("SELECT Guesses.date, Guesses.score, Guesses.game, Users.username FROM Guesses JOIN Users ON Guesses.user_id = Users.id ORDER BY date DESC").fetchall()
    db.close()
    return guesses

def CheckLogin(username, password):

    db = GetDB()

    # Ask the database for a single user matching the provided name
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()

    # Do they exist?
    if user is not None:
        # OK they exist, is their password correct
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        if user['password'] == password_hash:
            # They got it right, return their details 
            return user
        
    # If we get here, the username or password failed.
    return None

def RegisterUser(username, password):

    # Check if they gave us a username and password
    if username is None or password is None or username.strip() == "" or password.strip() == "":
        return False

    # Check password strength: minimum 8 characters
    if len(password) < 8:
        return False

    # Check if username already exists
    db = GetDB()
    existing_user = db.execute("SELECT id FROM Users WHERE username=?", (username,)).fetchone()
    if existing_user:
        db.close()
        return False

    # Attempt to add them to the database
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, password_hash,))
    db.commit()
    db.close()

    return True

##################################
### New code starts here
##################################

def AddGuess(user_id, date, game, score):
   
    # Check if any boxes were empty
    if date is None or game is None or score is None:
        return False
    
    # Check for empty strings
    if date.strip() == "" or game.strip() == "" or str(score).strip() == "":
        return False
    
    # Validate date format (YYYY-MM-DD)
    try:
        from datetime import datetime
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    
    # Validate score: should be positive integer
    try:
        score_int = int(score)
        if score_int <= 0:
            return False
    except ValueError:
        return False
   
    # Get the DB and add the guess
    db = GetDB()
    db.execute("INSERT INTO Guesses(user_id, date, game, score) VALUES (?, ?, ?, ?)",
               (user_id, date, game, score_int,))
    db.commit()
    db.close()

    return True

##################################
### New code ends here
##################################
