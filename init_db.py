import sqlite3

def init_db():
    conn = sqlite3.connect('fruitshop.db')
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS accounts')
    cursor.execute('DROP TABLE IF EXISTS agrahi')

    # Create accounts table
    cursor.execute('''
    CREATE TABLE accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        account_name TEXT NOT NULL,
        new_item INTEGER DEFAULT 0,
        jama INTEGER DEFAULT 0,
        total_amount INTEGER DEFAULT 0,
        remaining INTEGER DEFAULT 0
    )
    ''')

    # Create agrahi table
    cursor.execute('''
    CREATE TABLE agrahi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_name TEXT NOT NULL,
        date TEXT NOT NULL,
        pichla INTEGER DEFAULT 0,
        new_item INTEGER DEFAULT 0,
        jama INTEGER DEFAULT 0,
        baqaya INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized successfully!')