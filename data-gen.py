import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data():
    """Generate mixed real and sample test data."""
    db = connect_db()
    cursor = db.cursor()

    # Ensure the contacts table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        )
    ''')

    # Real contacts
    real_contacts = [
        ('Marie Alla', '513-888-2342'),
        ('John Smith', '305-456-7890'),
        ('Lisa Ray', '312-555-1212')
    ]

    # Sample/test contacts
    sample_contacts = [
        ('Sample Contact 1', '999-000-1001'),
        ('Sample Contact 2', '999-000-1002'),
        ('Sample Contact 3', '999-000-1003')
    ]

    # Insert into table
    for name, phone in real_contacts + sample_contacts:
        cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))

    db.commit()
    print(f'{len(real_contacts) + len(sample_contacts)} contacts added.')
    db.close()

if __name__ == '__main__':
    generate_test_data()
