import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    db = connect_db()

    # Ensure table exists
    db.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')

    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        address = f'{i} Example Street'
        db.execute('INSERT INTO contacts (name, phone, address) VALUES (?, ?, ?)', (name, phone, address))

    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)
