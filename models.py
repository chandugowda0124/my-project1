import sqlite3

def init_db():
    conn = sqlite3.connect('rules.db')
    cursor = conn.cursor()

    # Create rules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule TEXT,
            ast_repr TEXT
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()  # Initialize the database
