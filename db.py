import re
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def GetDB():
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row
    return db


def GetAllEntries():
    db = GetDB()
    entries = db.execute("""
        SELECT Entries.date, Entries.character_name, Entries.rating, Entries.note,
               Users.username, Users.sanrio_character
        FROM Entries
        JOIN Users ON Entries.user_id = Users.id
        ORDER BY date DESC
    """).fetchall()
    db.close()
    return entries


def GetUserById(user_id):
    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE id=?", (user_id,)).fetchone()
    db.close()
    return user


def CheckLogin(username, password):
    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()
    db.close()

    if user is not None and check_password_hash(user["password"], password):
        return user

    return None


def RegisterUser(username, password, sanrio_character):
    if username is None or password is None or sanrio_character is None:
        return False

    username = username.strip()
    password = password.strip()
    sanrio_character = sanrio_character.strip()

    if username == "" or password == "" or sanrio_character == "":
        return False

    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,20}", username):
        return False

    if len(password) < 8:
        return False

    allowed_characters = [
        "Hello Kitty",
        "Aggretsuko",
        "My Melody",
        "Kuromi",
        "Cinnamoroll",
        "Pompompurin",
        "Keroppi"
    ]

    if sanrio_character not in allowed_characters:
        return False

    db = GetDB()
    existing_user = db.execute("SELECT id FROM Users WHERE username=?", (username,)).fetchone()
    if existing_user:
        db.close()
        return False

    password_hash = generate_password_hash(password)
    db.execute(
        "INSERT INTO Users(username, password, sanrio_character) VALUES(?, ?, ?)",
        (username, password_hash, sanrio_character)
    )
    db.commit()
    db.close()
    return True


def AddEntry(user_id, date, character_name, rating, note):
    if user_id is None or date is None or character_name is None or rating is None or note is None:
        return False

    date = date.strip()
    character_name = character_name.strip()
    rating = str(rating).strip()
    note = note.strip()

    if date == "" or character_name == "" or rating == "" or note == "":
        return False

    allowed_characters = [
        "Hello Kitty",
        "Aggretsuko",
        "My Melody",
        "Kuromi",
        "Cinnamoroll",
        "Pompompurin",
        "Keroppi"
    ]

    if character_name not in allowed_characters:
        return False

    if len(note) > 150:
        return False

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False

    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            return False
    except ValueError:
        return False

    db = GetDB()
    db.execute(
        "INSERT INTO Entries(user_id, date, character_name, rating, note) VALUES (?, ?, ?, ?, ?)",
        (user_id, date, character_name, rating_int, note)
    )
    db.commit()
    db.close()
    return True