import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    """Generate test contacts for the contacts table."""
    db = connect_db()
    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        address = f'{i} Example St, City, ST 1234{i}'
        db.execute('INSERT INTO contacts (name, phone, address) VALUES (?, ?, ?)', (name, phone, address))
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)
