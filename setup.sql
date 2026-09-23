-- Uncomment to reset DB
-- DROP TABLE IF EXISTS note;
-- DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS note(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);