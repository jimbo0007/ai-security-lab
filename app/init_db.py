import sqlite3

db = sqlite3.connect("users.db")

db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

db.execute("""
INSERT OR IGNORE INTO users (id, username, email)
VALUES (1, 'alice', 'alice@example.com')
""")

db.execute("""
INSERT OR IGNORE INTO users (id, username, email)
VALUES (2, 'bob', 'bob@example.com')
""")

db.commit()
db.close()

print("Database initialized")
