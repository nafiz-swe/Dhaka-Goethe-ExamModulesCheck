import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run this function once to create the database.
create_db()
import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run this function once to create the database.
create_db()
