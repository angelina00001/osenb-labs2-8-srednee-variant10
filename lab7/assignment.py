import sqlite3

def assignment_code():
    conn = sqlite3.connect("my.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        )
    """)

    cur.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", 
                ('Мария', 25, 'maria@example.com'))

    conn.commit()
    cur.close()
    conn.close()
