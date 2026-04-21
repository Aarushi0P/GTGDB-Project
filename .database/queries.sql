DROP TABLE IF EXISTS Entries;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    sanrio_character TEXT NOT NULL
);

CREATE TABLE Entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    character_name TEXT NOT NULL,
    rating INTEGER NOT NULL,
    note TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO Users (username, password, sanrio_character) VALUES
('syykuno', 'pbkdf2:sha256:600000$demo1$replace_with_real_hash', 'Aggretsuko'),
('whatishellokitty', 'pbkdf2:sha256:600000$demo2$replace_with_real_hash', 'Hello Kitty'),
('kuromicoder', 'pbkdf2:sha256:600000$demo3$replace_with_real_hash', 'Kuromi'),
('mymelodrama', 'pbkdf2:sha256:600000$demo4$replace_with_real_hash', 'My Melody'),
('cinnabun.exe', 'pbkdf2:sha256:600000$demo5$replace_with_real_hash', 'Cinnamoroll'),
('purinpudding', 'pbkdf2:sha256:600000$demo6$replace_with_real_hash', 'Pompompurin'),
('frogotchi', 'pbkdf2:sha256:600000$demo7$replace_with_real_hash', 'Keroppi');

INSERT INTO Entries (user_id, date, character_name, rating, note) VALUES
(1, '2026-04-15', 'Aggretsuko', 5, 'Best stress icon ever.'),
(2, '2026-04-15', 'Hello Kitty', 4, 'Classic and instantly recognisable.'),
(3, '2026-04-16', 'Kuromi', 5, 'Chaos but cute.'),
(4, '2026-04-16', 'My Melody', 4, 'Soft pink perfection.'),
(5, '2026-04-17', 'Cinnamoroll', 5, 'Looks like a marshmallow cloud.'),
(6, '2026-04-17', 'Pompompurin', 4, 'Tiny beret, huge energy.'),
(7, '2026-04-18', 'Keroppi', 4, 'Underrated frog king.');